# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: prephouse.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='prephouse.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0fprephouse.proto\"\x15\n\x05Video\x12\x0c\n\x04link\x18\x01 \x01(\t\"\x8b\x01\n\x08\x46\x65\x65\x64\x62\x61\x63k\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\x11\n\x04text\x18\x02 \x01(\tH\x00\x88\x01\x01\x12\r\n\x05score\x18\x03 \x01(\x02\x12\x16\n\ttimeStart\x18\x04 \x01(\x02H\x01\x88\x01\x01\x12\x14\n\x07timeEnd\x18\x05 \x01(\x02H\x02\x88\x01\x01\x42\x07\n\x05_textB\x0c\n\n_timeStartB\n\n\x08_timeEnd27\n\x0fPrephouseEngine\x12$\n\x0bGetFeedback\x12\x06.Video\x1a\t.Feedback\"\x00\x30\x01\x62\x06proto3'
)




_VIDEO = _descriptor.Descriptor(
  name='Video',
  full_name='Video',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='link', full_name='Video.link', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=19,
  serialized_end=40,
)


_FEEDBACK = _descriptor.Descriptor(
  name='Feedback',
  full_name='Feedback',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='Feedback.type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='text', full_name='Feedback.text', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='score', full_name='Feedback.score', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='timeStart', full_name='Feedback.timeStart', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='timeEnd', full_name='Feedback.timeEnd', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='_text', full_name='Feedback._text',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
    _descriptor.OneofDescriptor(
      name='_timeStart', full_name='Feedback._timeStart',
      index=1, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
    _descriptor.OneofDescriptor(
      name='_timeEnd', full_name='Feedback._timeEnd',
      index=2, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=43,
  serialized_end=182,
)

_FEEDBACK.oneofs_by_name['_text'].fields.append(
  _FEEDBACK.fields_by_name['text'])
_FEEDBACK.fields_by_name['text'].containing_oneof = _FEEDBACK.oneofs_by_name['_text']
_FEEDBACK.oneofs_by_name['_timeStart'].fields.append(
  _FEEDBACK.fields_by_name['timeStart'])
_FEEDBACK.fields_by_name['timeStart'].containing_oneof = _FEEDBACK.oneofs_by_name['_timeStart']
_FEEDBACK.oneofs_by_name['_timeEnd'].fields.append(
  _FEEDBACK.fields_by_name['timeEnd'])
_FEEDBACK.fields_by_name['timeEnd'].containing_oneof = _FEEDBACK.oneofs_by_name['_timeEnd']
DESCRIPTOR.message_types_by_name['Video'] = _VIDEO
DESCRIPTOR.message_types_by_name['Feedback'] = _FEEDBACK
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Video = _reflection.GeneratedProtocolMessageType('Video', (_message.Message,), {
  'DESCRIPTOR' : _VIDEO,
  '__module__' : 'prephouse_pb2'
  # @@protoc_insertion_point(class_scope:Video)
  })
_sym_db.RegisterMessage(Video)

Feedback = _reflection.GeneratedProtocolMessageType('Feedback', (_message.Message,), {
  'DESCRIPTOR' : _FEEDBACK,
  '__module__' : 'prephouse_pb2'
  # @@protoc_insertion_point(class_scope:Feedback)
  })
_sym_db.RegisterMessage(Feedback)



_PREPHOUSEENGINE = _descriptor.ServiceDescriptor(
  name='PrephouseEngine',
  full_name='PrephouseEngine',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=184,
  serialized_end=239,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetFeedback',
    full_name='PrephouseEngine.GetFeedback',
    index=0,
    containing_service=None,
    input_type=_VIDEO,
    output_type=_FEEDBACK,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_PREPHOUSEENGINE)

DESCRIPTOR.services_by_name['PrephouseEngine'] = _PREPHOUSEENGINE

# @@protoc_insertion_point(module_scope)
