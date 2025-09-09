from typing import Iterable
from src.etl.abstractions import Transformer
from src.etl.models import Event, Entity, Airline, Flight, Passenger
from src.etl.schema_mapper import SchemaMapper

class OntologyTransformer(Transformer):
    def __init__(self, schema_mapper: SchemaMapper):
        self.schema_mapper = schema_mapper
        self.mapping_cache = {}

    def transform(self, data: Iterable[Event | Entity]) -> Iterable[Event | Entity]:
        for item in data:
            if isinstance(item, Event) and item.event_type == 'flight':
                if 'flight' not in self.mapping_cache:
                    source_columns = list(item.payload.keys())
                    target_schema = Flight
                    self.mapping_cache['flight'] = self.schema_mapper.get_schema_mapping(source_columns, target_schema)
                mapping = self.mapping_cache['flight']

                # This is a simplified transformation. A more robust implementation
                # would handle data type conversions and validations.
                flight_data = {target_key: item.payload.get(source_key) for source_key, target_key in mapping.items()}
                
                # Create Passenger object
                passenger_data = {}
                if 'passngr_nm' in item.payload:
                    passenger_data['name'] = item.payload['passngr_nm']

                for key in list(Passenger.model_fields.keys()):
                    if key in flight_data:
                        passenger_data[key] = flight_data.pop(key)
                
                flight_data['passenger'] = Passenger(**passenger_data)

                yield Flight(**flight_data)

            elif isinstance(item, Entity) and item.entity_type == 'airline':
                if 'airline' not in self.mapping_cache:
                    source_columns = list(item.attributes.keys())
                    target_schema = Airline
                    self.mapping_cache['airline'] = self.schema_mapper.get_schema_mapping(source_columns, target_schema)
                mapping = self.mapping_cache['airline']

                airline_data = {target_key: item.attributes.get(source_key) for source_key, target_key in mapping.items()}
                yield Airline(**airline_data)
            else:
                yield item
