import logging
import math

from cmdb.models import session, Schema, Field, Entity, Value, FieldMeta

logger = logging.getLogger(__name__)


# schema接口
# 返回一个schema对象
def get_schema_by_name(name: str, deleted: bool = False):
    query = session.query(Schema).filter(Schema.name == name.strip())
    if not deleted:
        query = query.filter(Schema.deleted == False)
    return query.first()


# 增加一个schema
def add_schema(name: str, desc: str = None):
    schema = Schema()
    schema.name = name.strip()
    schema.desc = desc
    session.add(schema)
    try:
        session.commit()
        return schema
    except Exception as e:
        session.rollback()
        logger.error('Fail to add a new schema {}. Error: {}'.format(name, e))


# 删除使用id，id唯一，比使用name删除好
def delete_schema(id: int):
    try:
        schema = session.query(Schema).filter((Schema.id == id) & (Schema.deleted == False))
        if schema:
            schema.deleted = True
            session.add(schema)
            try:
                session.commit()
                return schema
            except Exception as e:
                session.rollback()
                raise e
        else:
            raise ValueError('Wrong ID {}'.format(id))
    except Exception as e:
        logger.error('Fail to del a schema. id = {}. Error: {}'.format(id, e))


# 列出所有逻辑表
def list_schema_bak(page: int, size: int, deleted: bool = False):
    try:
        query = session.query(Schema)
        if not deleted:
            query = query.filter(Schema.deleted == False)
        page = page if page > 0 else 1
        size = size if 0 < size < 101 else 20
        count = query.count()
        pages = math.ceil(count / size)
        result = query.limit(size).offset(size * (page - 1)).all()
        return result, (page, size, count, pages)
    except Exception as e:
        logger.error()


# 列出所有逻辑表
def list_schema(page: int = 1, size: int = 20, deleted: bool = False):
    query = session.query(Schema)
    if not deleted:
        query = query.filter(Schema.deleted == False)
    return paginate(page, size, query)


# 通用分页函数
def paginate(page, size, query):
    try:
        page = page if page > 0 else 1
        size = size if 0 < size < 101 else 20
        count = query.count()
        pages = math.ceil(count / size)
        result = query.limit(size).offset(size * (page - 1)).all()
        return result, (page, size, count, pages)
    except Exception as e:
        logger.error("{}".format(e))


# field接口
# 获取字段
def get_field(schema_name, field_name, deleted=False):
    schema = get_schema_by_name(schema_name)
    if not schema:
        raise ValueError('{} is not a Tablename'.format(schema_name))
    query = session.query(Field).filter((Field.schema_id == schema.id) & (Field.name == field_name))
    if not deleted:
        query = query.filter(Field.deleted == False)
    return query.first()


# 逻辑表是否已经使用
def table_used(schema_id, deleted=False):
    query = session.query(Entity).filter(Entity.schema_id == schema_id)
    if not deleted:
        query = query.filter(Entity.deleted == False)
    return query.first() is not None


# 直接添加字段
def _add_field(field: Field):
    session.add(field)
    try:
        session.commit()
        return field
    except Exception as e:
        session.rollback()
        logger.error('Failed to add a field {}. Error: {}'.format(field.name, e))
        # 2种情况:1完全新增 2已有表增加字段


def add_field(schema_name, name, meta):
    schema = get_schema_by_name(schema_name)
    if not schema:
        raise ValueError('{} is not a Tablename'.format(schema_name))
    # 解析meta，from ..models import FieldMeta
    meta_data = FieldMeta(meta)
    field = Field()
    field.name = name.strip()
    field.schema_id = schema.id
    field.meta = meta  # 能解析成功说明符合格式要求 # ref_id 引用
    if meta_data.reference:
        ref = get_field(meta_data.reference.schema, meta_data.reference.field)
        if not ref:
            raise TypeError('Wrong Reference {}.{}'.format(meta_data.reference.schema, meta_data.reference.field))
        field.ref_id = ref.id
    # 判断字段是否已经使用
    if not table_used(schema.id):  # 未使用的逻辑表，直接加字段
        return _add_field(field)
    # 已使用的逻辑表
    if meta_data.nullable:  # 可以为空，直接加字段
        return _add_field(field)
    # 到这里已经有一个隐含条件即不可为空
    if meta_data.unique:  # 必须唯一
        # 当前的条件是 对一个正在使用的逻辑表加字段不可以为空又要唯一，做不到
        raise TypeError('This field is required an unique.')
        # 到这里的隐含条件是，不可以为空，但可以不唯一
        if not meta_data.default:  # 没有缺省值
            raise TypeError('This field requires a default value.')
        else:
            # 为逻辑表所有记录增加字段，操作entity表
            entities = session.query(Entity).filter((Entity.schema_id == schema.id) & (Entity.deleted == False)).all()
            for entity in entities:  # value表新增记录
                value = Value()
                value.entity_id = entity.id
                value.field = field
                value.value = meta_data.default
                session.add(value)
            return _add_field(field)
    # 到这里的隐含条件是，不可以为空，但可以不唯一
    if not meta_data.default:  # 没有缺省值
        raise TypeError('This field requires a default value.')
    else:
        # 为逻辑表所有记录增加字段，操作entity表
        for entity in iter_entities(schema.id):  # value表新增记录
            value = Value()
            value.entity_id = entity.id
            value.field = field
            value.value = meta_data.default
            session.add(value)
        return _add_field(field)


def iter_entities(schema_id, patch=100):
    page = 1
    while True:
        query = session.query(Entity).filter((Entity.schema_id == schema_id) & (Entity.deleted == False))
        result = query.limit(patch).offset((page - 1) * patch).all()
        if not result:
            return None
        yield from result
        page += 1

#总结
# 本项目通过mysql数据库设计，实现一个复杂的cmdb
# 目前的这个cmdb功能还是比较简陋的，很多的功能还没有实现锁的机制等
# 但是目前为止，基本功能已经可心实现和完成了，其实生产环境中真正的功能也就是现在这样了
# 及时花了很大的功夫，把更加复杂的功能实现了，也未能有用户使用
# 本项目学习目的
# 学习数据库设计
# 进一步巩固SQLAlchemy使用
# 学习Service层的写法
# 巩固日志的使用
# 学习插件化开发思想
# 学习复杂的逻辑设计，开发，锻炼严谨的思维能力，应用到项目开发中