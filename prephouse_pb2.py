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
  serialized_pb=b'\n\x0fprephouse.proto\"`\n\tMediaList\x12\x12\n\naudio_link\x18\x01 \x01(\t\x12\x17\n\x0ftranscript_link\x18\x02 \x01(\t\x12\x17\n\nvideo_link\x18\x03 \x01(\tH\x00\x88\x01\x01\x42\r\n\x0b_video_link\"\xb1\x03\n\x08\x46\x65\x65\x64\x62\x61\x63k\x12#\n\x08\x63\x61tegory\x18\x01 \x01(\x0e\x32\x11.Feedback.Feature\x12\x18\n\x0bsubcategory\x18\x02 \x01(\tH\x00\x88\x01\x01\x12\x14\n\x07\x63omment\x18\x03 \x01(\tH\x01\x88\x01\x01\x12\x0e\n\x06result\x18\x04 \x01(\x02\x12\x17\n\nconfidence\x18\x05 \x01(\x05H\x02\x88\x01\x01\x12\x17\n\ntime_start\x18\x06 \x01(\x02H\x03\x88\x01\x01\x12\x15\n\x08time_end\x18\x07 \x01(\x02H\x04\x88\x01\x01\"\xaf\x01\n\x07\x46\x65\x61ture\x12\x17\n\x13\x46\x45\x41TURE_UNSPECIFIED\x10\x00\x12\x11\n\rFEATURE_PAUSE\x10\x01\x12\x12\n\x0e\x46\x45\x41TURE_VOLUME\x10\x02\x12\x11\n\rFEATURE_LIGHT\x10\x03\x12\x10\n\x0c\x46\x45\x41TURE_GAZE\x10\x04\x12\x13\n\x0f\x46\x45\x41TURE_EMOTION\x10\x05\x12\x11\n\rFEATURE_PITCH\x10\x06\x12\x17\n\x13\x46\x45\x41TURE_FILLER_WORD\x10\x07\x42\x0e\n\x0c_subcategoryB\n\n\x08_commentB\r\n\x0b_confidenceB\r\n\x0b_time_startB\x0b\n\t_time_end\"Z\n\x0c\x46\x65\x65\x64\x62\x61\x63kList\x12\x1b\n\x08\x66\x65\x65\x64\x62\x61\x63k\x18\x01 \x03(\x0b\x32\t.Feedback\x12\x16\n\x0e\x65ngine_version\x18\x02 \x01(\t\x12\x15\n\rengine_config\x18\x03 \x01(\t2m\n\x0fPrephouseEngine\x12*\n\x0bGetFeedback\x12\n.MediaList\x1a\r.FeedbackList\"\x00\x12.\n\x0fGetMockFeedback\x12\n.MediaList\x1a\r.FeedbackList\"\x00\x62\x06proto3'
)



_FEEDBACK_FEATURE = _descriptor.EnumDescriptor(
  name='Feature',
  full_name='Feedback.Feature',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='FEATURE_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FEATURE_PAUSE', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FEATURE_VOLUME', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FEATURE_LIGHT', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FEATURE_GAZE', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FEATURE_EMOTION', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FEATURE_PITCH', index=6, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FEATURE_FILLER_WORD', index=7, number=7,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=305,
  serialized_end=480,
)
_sym_db.RegisterEnumDescriptor(_FEEDBACK_FEATURE)


_MEDIALIST = _descriptor.Descriptor(
  name='MediaList',
  full_name='MediaList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='audio_link', full_name='MediaList.audio_link', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='transcript_link', full_name='MediaList.transcript_link', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='video_link', full_name='MediaList.video_link', index=2,
      number=3, type=9, cpp_type=9, label=1,
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
    _descriptor.OneofDescriptor(
      name='_video_link', full_name='MediaList._video_link',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=19,
  serialized_end=115,
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
      name='category', full_name='Feedback.category', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='subcategory', full_name='Feedback.subcategory', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='comment', full_name='Feedback.comment', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='result', full_name='Feedback.result', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='confidence', full_name='Feedback.confidence', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='time_start', full_name='Feedback.time_start', index=5,
      number=6, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='time_end', full_name='Feedback.time_end', index=6,
      number=7, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _FEEDBACK_FEATURE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='_subcategory', full_name='Feedback._subcategory',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
    _descriptor.OneofDescriptor(
      name='_comment', full_name='Feedback._comment',
      index=1, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
    _descriptor.OneofDescriptor(
      name='_confidence', full_name='Feedback._confidence',
      index=2, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
    _descriptor.OneofDescriptor(
      name='_time_start', full_name='Feedback._time_start',
      index=3, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
    _descriptor.OneofDescriptor(
      name='_time_end', full_name='Feedback._time_end',
      index=4, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=118,
  serialized_end=551,
)


_FEEDBACKLIST = _descriptor.Descriptor(
  name='FeedbackList',
  full_name='FeedbackList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='feedback', full_name='FeedbackList.feedback', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='engine_version', full_name='FeedbackList.engine_version', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='engine_config', full_name='FeedbackList.engine_config', index=2,
      number=3, type=9, cpp_type=9, label=1,
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
  serialized_start=553,
  serialized_end=643,
)

_MEDIALIST.oneofs_by_name['_video_link'].fields.append(
  _MEDIALIST.fields_by_name['video_link'])
_MEDIALIST.fields_by_name['video_link'].containing_oneof = _MEDIALIST.oneofs_by_name['_video_link']
_FEEDBACK.fields_by_name['category'].enum_type = _FEEDBACK_FEATURE
_FEEDBACK_FEATURE.containing_type = _FEEDBACK
_FEEDBACK.oneofs_by_name['_subcategory'].fields.append(
  _FEEDBACK.fields_by_name['subcategory'])
_FEEDBACK.fields_by_name['subcategory'].containing_oneof = _FEEDBACK.oneofs_by_name['_subcategory']
_FEEDBACK.oneofs_by_name['_comment'].fields.append(
  _FEEDBACK.fields_by_name['comment'])
_FEEDBACK.fields_by_name['comment'].containing_oneof = _FEEDBACK.oneofs_by_name['_comment']
_FEEDBACK.oneofs_by_name['_confidence'].fields.append(
  _FEEDBACK.fields_by_name['confidence'])
_FEEDBACK.fields_by_name['confidence'].containing_oneof = _FEEDBACK.oneofs_by_name['_confidence']
_FEEDBACK.oneofs_by_name['_time_start'].fields.append(
  _FEEDBACK.fields_by_name['time_start'])
_FEEDBACK.fields_by_name['time_start'].containing_oneof = _FEEDBACK.oneofs_by_name['_time_start']
_FEEDBACK.oneofs_by_name['_time_end'].fields.append(
  _FEEDBACK.fields_by_name['time_end'])
_FEEDBACK.fields_by_name['time_end'].containing_oneof = _FEEDBACK.oneofs_by_name['_time_end']
_FEEDBACKLIST.fields_by_name['feedback'].message_type = _FEEDBACK
DESCRIPTOR.message_types_by_name['MediaList'] = _MEDIALIST
DESCRIPTOR.message_types_by_name['Feedback'] = _FEEDBACK
DESCRIPTOR.message_types_by_name['FeedbackList'] = _FEEDBACKLIST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MediaList = _reflection.GeneratedProtocolMessageType('MediaList', (_message.Message,), {
  'DESCRIPTOR' : _MEDIALIST,
  '__module__' : 'prephouse_pb2'
  # @@protoc_insertion_point(class_scope:MediaList)
  })
_sym_db.RegisterMessage(MediaList)

Feedback = _reflection.GeneratedProtocolMessageType('Feedback', (_message.Message,), {
  'DESCRIPTOR' : _FEEDBACK,
  '__module__' : 'prephouse_pb2'
  # @@protoc_insertion_point(class_scope:Feedback)
  })
_sym_db.RegisterMessage(Feedback)

FeedbackList = _reflection.GeneratedProtocolMessageType('FeedbackList', (_message.Message,), {
  'DESCRIPTOR' : _FEEDBACKLIST,
  '__module__' : 'prephouse_pb2'
  # @@protoc_insertion_point(class_scope:FeedbackList)
  })
_sym_db.RegisterMessage(FeedbackList)



_PREPHOUSEENGINE = _descriptor.ServiceDescriptor(
  name='PrephouseEngine',
  full_name='PrephouseEngine',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=645,
  serialized_end=754,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetFeedback',
    full_name='PrephouseEngine.GetFeedback',
    index=0,
    containing_service=None,
    input_type=_MEDIALIST,
    output_type=_FEEDBACKLIST,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetMockFeedback',
    full_name='PrephouseEngine.GetMockFeedback',
    index=1,
    containing_service=None,
    input_type=_MEDIALIST,
    output_type=_FEEDBACKLIST,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_PREPHOUSEENGINE)

DESCRIPTOR.services_by_name['PrephouseEngine'] = _PREPHOUSEENGINE

# @@protoc_insertion_point(module_scope)
