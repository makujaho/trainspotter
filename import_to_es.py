#!/usr/bin/env python

import os
import sys
import json
import datetime
from elasticsearch import Elasticsearch
from trainspotter import utils

if len(sys.argv) < 2:
    print('usage: import_to_es.py [logpath]')
    os.exit(255)

trainspotter_log_path = sys.argv[1]
print('Using log path %s' % trainspotter_log_path)

try:
    es = Elasticsearch(
        [
            'https://user:pass@elastic.example.com',
            'http://192.168.255.1:9200',
            'http://192.168.255.2:9200',
            'http://192.168.255.3:9200',
        ],
        sniff_on_start=True,
        sniff_on_connection_fail=True,
        sniffer_timeout=120,
        timeout=1200,
        verify_certs=True
    )
except Exception as e:
    print('Could not connect to ES')
    print(e)


for subdir, dirs, files in os.walk(trainspotter_log_path):
    files.sort()
    for file in files:
        print('Processing: %s/%s' % (subdir, file))

        year = subdir.split('/')[-3].split('-')[-1]
        month = subdir.split('/')[-2].split('-')[-1]
        day = subdir.split('/')[-1]

        index_name = 'trainspotter-' + '-'.join([year, month, day])

        mapping = {
            'train': {
                '_all': {'enabled': False},
                '_source': {'enabled': True},
                'properties': {
                    'cid': {
                        'type': 'string',
                        'index': 'not_analyzed',
                        'norms': {'enabled': False}
                    },
                    'timestamp': {'type': 'date', 'norms': {'enabled': False}},
                    'location': {
                        'type': 'geo_point',
                        'fielddata': {
                            'lat_lon': True,
                            'format': 'compressed',
                            'precision': '3m'
                        },
                        'norms': {'enabled': False}
                    },
                    'name': {
                        'type': 'string',
                        'analyzer': 'keyword',
                        'fielddata': {
                            'format': 'fst'
                        },
                        'norms': {'enabled': False},
                        'fields': {
                            'raw': {'type': 'string', 'index': 'not_analyzed'}
                        }
                    },
                    'train_id': {
                        'type': 'string',
                        'analyzer': 'keyword',
                        'index': 'analyzed',
                        'norms': {'enabled': False},
                        'fields': {
                            'raw': {
                                'type': 'string',
                                'index': 'not_analyzed',
                                'norms': {'enabled': False}
                            }
                        }
                    },
                    'pstopname': {
                        'type': 'string',
                        'index': 'analyzed',
                        'fields': {
                            'raw': {'type': 'string', 'index': 'not_analyzed'}
                        }
                    },
                    'lstopname': {
                        'type': 'string',
                        'index': 'analyzed',
                        'fields': {
                            'raw': {'type': 'string', 'index': 'not_analyzed'}
                        }
                    },
                    'productclass': {
                        'type': 'integer',
                        'norms': {'enabled': False}
                    },
                    'productclass.name': {
                        'type': 'string',
                        'analyzer': 'keyword',
                        'index': 'analyzed',
                        'fields': {
                            'raw': {'type': 'string', 'index': 'not_analyzed'}
                        }
                    },
                    'y_enc': {
                        'type': 'integer',
                        'index': 'not_analyzed',
                        'norms': {'enabled': False},
                        'include_in_all': False
                    },
                    'x_enc': {
                        'type': 'integer',
                        'index': 'not_analyzed',
                        'norms': {'enabled': False},
                        'include_in_all': False
                    },
                    'delay': {
                        'type': 'integer',
                        'null_value': 0,
                        'index': 'not_analyzed',
                        'norms': {'enabled': False}
                    },
                    'direction': {
                        'type': 'integer',
                        'index': 'not_analyzed',
                        'norms': {'enabled': False},
                        'include_in_all': False
                    },
                    'pstopno': {
                        'type': 'integer',
                        'index': 'not_analyzed',
                        'norms': {'enabled': False}
                    },
                    'lstopno': {
                        'type': 'integer',
                        'index': 'not_analyzed',
                        'norms': {'enabled': False}
                    }
                }
            }
        }

        with open(subdir + '/' + file) as f:
            bulk_data = []
            for line in f:
                try:
                    data = json.loads(line)

                    if 'time' not in data:
                        hour = file.split('-')[-3]
                        minute = file.split('-')[-2]
                        second = file.split('-')[-1].split('.')[-2]

                        data['time'] = '%s:%s:%s' % (hour, minute, second)

                    timestamp = '%s %s' % (data['dateRef'], data['time'])

                    data['train_id'] = data.pop('id')
                    data['timestamp'] = datetime.datetime.strptime(
                        timestamp, '%d.%m.%y %H:%M:%S')
                    data['location'] = {
                        'lon': utils.convert_coord(data['x']),
                        'lat': utils.convert_coord(data['y'])
                    }
                    data['productclass.name'] = utils.get_productclass_name(
                        data['productclass'])
                    data['cid'] = '%s-%s' % (
                        data['time'],
                        data['train_id'].replace('/', '-'))

                    bulk_dict = {
                        'create': {
                            '_index': index_name,
                            '_type': 'train',
                            '_id': data['cid']
                        }
                    }

                    bulk_data.append(bulk_dict)
                    bulk_data.append(data)
                except Exception as e:
                    print('An error occured:')
                    print(e)

            print('Creating index if it doesn\'t exist')
            es.indices.create(index=index_name,
                              body={'mappings': mapping},
                              ignore=400)

            print('Throwing up large chunks of data into cluster')
            try:
                es.bulk(index=index_name, body=bulk_data)
            except Exception as e:
                print(e)
