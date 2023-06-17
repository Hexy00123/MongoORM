from bson import ObjectId


class Factory:
    def __init__(self, dtype: type):
        self.dtype = dtype

    def create_inst(self, **kwargs):
        '''
        Description: Creates an instance of the data type with the provided keyword arguments.
        Parameters:
          - kwargs: Keyword arguments for initializing the instance.
        Returns:
          - The created instance.
        '''

        class Data(self.dtype):
            def __init__(obj, **kwargs):
                if kwargs:
                    obj._id = kwargs["_id"]
                    obj.__is_changed = False
                    del kwargs["_id"]
                    super().__init__(**kwargs)

            def id(obj):
                return str(obj._id)

            def __str__(obj):
                return f"{str(self.dtype.__name__)}: {'{'}{', '.join([f'{field}={getattr(obj, field)}' for field in self.dtype.__annotations__])}{'}'}"

            def __repr__(obj):
                return obj.__str__()

            def jsonify(obj):
                def convert_to_json(value):
                    if isinstance(value, ObjectId):
                        return str(value)
                    elif isinstance(value, list):
                        return [convert_to_json(item) for item in value]
                    elif isinstance(value, dict):
                        return {key: convert_to_json(val) for key, val in value.items()}
                    elif isinstance(value, bytes):
                        raise TypeError("Objects with bytes field cannot be dumped to the JSON")
                    else:
                        return value

                result = {
                    'id': obj.id()
                }
                for field in self.dtype.__annotations__:
                    result[field] = convert_to_json(getattr(obj, field))

                return result

        if self.dtype.__init__ != object.__init__:
            inst = Data(**kwargs)
        else:
            inst = Data()
            for field in kwargs:
                setattr(inst, field, kwargs[field])
        return inst


if __name__ == '__main__':
    from pprint import pprint


    class Test:
        field1: int
        field2: ObjectId
        field3: list[ObjectId]
        field4: list[list[ObjectId]]
        field5: dict[str: list[ObjectId]]


    f = Factory(Test)
    res = f.create_inst(_id=1,
                        field1=4,
                        field2=ObjectId("648b78d24c4b38560a352ce1"),
                        field3=[ObjectId("648b78d24c4b38560a352ce1"),
                                ObjectId("648b78d24c4b38560a352ce2")],
                        field4=[[ObjectId("648b78d24c4b38560a352ce1"), ObjectId("648b78d24c4b38560a352ce2")],
                                [ObjectId("648b78d24c4b38560a352ce3"), ObjectId("648b78d24c4b38560a352ce4")],
                                [ObjectId("648b78d24c4b38560a352ce5"), ObjectId("648b78d24c4b38560a352ce6")]],
                        field5={
                            '1': [ObjectId('648b78d24c4b38560a352ce1'), ObjectId("648b78d24c4b38560a352ce1")],
                            '2': [ObjectId('648b78d24c4b38560a352ce2'), ObjectId("648b78d24c4b38560a352ce2")],
                            '3': [ObjectId('648b78d24c4b38560a352ce3'), ObjectId("648b78d24c4b38560a352ce3")]
                        }).jsonify()

    pprint(res)
