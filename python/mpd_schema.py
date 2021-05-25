from collections import OrderedDict
from typing import Optional, List
import re
import typic
from typic.compat import Literal
from xmltodict import unparse

DURATION_PATTERN = re.compile(
    '^P(?P<year>\d+Y)?(?P<month>\d+M)?(?P<day>\d+D)?T(?P<hour>\d+H)?(?P<minute>\d+M)?(?P<second>\d+(?:.\d+)?S)?$')


@typic.klass
class DurationType:
    postive: Optional[bool] = typic.field(True)
    year: Optional[int] = typic.field(0)
    month: Optional[int] = typic.field(0)
    day: Optional[int] = typic.field(0)
    hour: Optional[int] = typic.field(0)
    minute: Optional[int] = typic.field(0)
    second: Optional[float] = typic.field(0)

    def loads(self, duration_str: Optional[str]) -> Optional['DurationType']:
        if duration_str is not None:
            matched = DURATION_PATTERN.match(duration_str)
            self.year = matched.group('year')[:-1] if matched.group('year') is not None else 0
            self.month = matched.group('month')[:-1] if matched.group('month') is not None else 0
            self.day = matched.group('day')[:-1] if matched.group('day') is not None else 0
            self.hour = matched.group('hour')[:-1] if matched.group('hour') is not None else 0
            self.minute = matched.group('minute')[:-1] if matched.group('minute') is not None else 0
            self.second = matched.group('second').strip('S') if matched.group('second') is not None else 0
            self.postive = not duration_str.startswith('-')
            return self
        return None

    def __str__(self):
        result = 'P'
        if self.year > 0:
            result += f'{self.year}Y'
        if self.month > 0:
            result += f'{self.month}M'
        if self.day > 0:
            result += f'{self.day}D'
        if self.hour + self.minute + self.second > 0:
            result += 'T'
            if self.hour > 0:
                result += f'{self.hour}H'
            if self.minute > 0:
                result += f'{self.minute}M'
            if self.second > 0:
                result += f'{self.second}S'
        if not self.postive:
            return f'-{result}'
        return result


@typic.constrained(ge=0, le=6)
class SAPType(int):
    ...


@typic.klass
class BaseURLType:
    service_location: Optional[str] = typic.field(None, name='@serviceLocation')
    byte_range: Optional[str] = typic.field(None, name='@byteRange')
    availability_time_offset: Optional[float] = typic.field(None, name='@availabilityTimeOffset')
    availability_time_complete: Optional[bool] = typic.field(None, name='@availabilityTimeComplete')
    text: Optional[str] = typic.field('', name='#text')

    def as_dict(self) -> OrderedDict:
        result = OrderedDict()
        if self.service_location is not None:
            result['@serviceLocation'] = self.service_location
        if self.byte_range is not None:
            result['@byteRange'] = self.byte_range
        if self.availability_time_offset is not None:
            result['@availabilityTimeOffset'] = self.availability_time_offset
        if self.availability_time_complete is not None:
            result['@availabilityTimeComplete'] = self.availability_time_complete
        if self.text is not None:
            result['#text'] = self.text
        return result


@typic.klass
class URLType:
    source_url: Optional[str] = typic.field(None, name='@sourceURL')
    range: Optional[str] = typic.field(None, name='@range')

    def as_dict(self) -> OrderedDict:
        result = OrderedDict()
        if self.source_url is not None:
            result['@sourceURL'] = self.source_url
        if self.range is not None:
            result['@range'] = self.range
        return result


@typic.klass
class SegmentBaseType:
    initialization: Optional[URLType] = typic.field(None, name='Initialization')
    representation_index: Optional[URLType] = typic.field(None, name='RepresentationIndex')

    timescale: Optional[int] = typic.field(None, name='@timescale')
    presentation_time_offset: Optional[int] = typic.field(None, name='@presentationTimeOffset')
    index_range: Optional[str] = typic.field(None, name='@indexRange')
    index_range_exact: Optional[bool] = typic.field(False, name='@indexRangeExact')
    availability_time_offset: Optional[float] = typic.field(None, name='@availabilityTimeOffset')
    availability_time_complete: Optional[bool] = typic.field(False, name='@availabilityTimeComplete')

    def as_dict(self) -> OrderedDict:
        result = OrderedDict()
        if self.initialization is not None:
            result['Initialization'] = self.initialization.as_dict()
        if self.representation_index is not None:
            result['RepresentationIndex'] = self.representation_index.as_dict()
        if self.timescale is not None:
            result['@timescale'] = self.timescale
        if self.presentation_time_offset is not None:
            result['@presentationTimeOffset'] = self.presentation_time_offset
        if self.index_range is not None:
            result['@indexRange'] = self.index_range
        if self.index_range_exact is not None:
            result['@indexRangeExact'] = self.index_range_exact
        if self.availability_time_offset is not None:
            result['@availabilityTimeOffset'] = self.availability_time_offset
        if self.availability_time_complete is not None:
            result['@availabilityTimeComplete'] = self.availability_time_complete
        return result


@typic.klass
class SingleSegmentTimelineType:
    d: Optional[int] = typic.field(None, name='@d')
    t: Optional[int] = typic.field(None, name='@t')
    n: Optional[int] = typic.field(None, name='@n')
    r: Optional[int] = typic.field(0, name='@r')

    def as_dict(self) -> OrderedDict:
        result = OrderedDict()
        if self.d is not None:
            result['@d'] = self.d
        if self.t is not None:
            result['@t'] = self.t
        if self.n is not None:
            result['@n'] = self.n
        if self.r is not None:
            result['@r'] = self.r
        return result


@typic.constrained(min_items=1)
class SegmentTimelineType(list):
    ...


@typic.klass
class MultipleSegmentBaseType(SegmentBaseType):
    segment_timeline: Optional[SegmentTimelineType] = typic.field(None, name='SegmentTimeline')
    bitstream_switching: Optional[BaseURLType] = typic.field(None, name='BitstreamSwitching')

    duration: Optional[int] = typic.field(None, name='@duration')
    start_number: Optional[int] = typic.field(None, name='@startNumber')

    def as_dict(self) -> OrderedDict:
        result = OrderedDict()
        if self.segment_timeline is not None:
            result['SegmentTimeline'] = self.segment_timeline.as_dict()
        if self.bitstream_switching is not None:
            result['BitstreamSwitching'] = self.bitstream_switching.as_dict()
        if self.duration is not None:
            result['@duration'] = self.duration
        if self.start_number is not None:
            result['@startNumber'] = self.start_number
        return result


@typic.klass
class SegmentTemplateType(MultipleSegmentBaseType):
    media: Optional[str] = typic.field(None, name='@media')
    index: Optional[str] = typic.field(None, name='@index')
    initialization: Optional[str] = typic.field(None, name='@initialization')
    bitstream_switching: Optional[str] = typic.field(None, name='@bitstreamSwitching')

    def as_dict(self) -> OrderedDict:
        result = OrderedDict()
        if self.media is not None:
            result['@media'] = self.media
        if self.index is not None:
            result['@index'] = self.index
        if self.initialization is not None:
            result['@initialization'] = self.initialization
        if self.bitstream_switching is not None:
            result['@bitstreamSwitching'] = self.bitstream_switching
        return result


@typic.klass
class SegmentURLType:
    media: Optional[str] = typic.field(None, name='@media')
    media_range: Optional[str] = typic.field(None, name='@mediaRange')
    index: Optional[str] = typic.field(None, name='@index')
    index_range: Optional[str] = typic.field(None, name='@indexRange')

    def as_dict(self) -> OrderedDict:
        result = OrderedDict()
        if self.media is not None:
            result['@media'] = self.media
        if self.media_range is not None:
            result['@mediaRange'] = self.media_range
        if self.index is not None:
            result['@index'] = self.index
        if self.index_range is not None:
            result['@indexRange'] = self.index_range
        return result


@typic.klass
class SegmentListType(MultipleSegmentBaseType):
    SegmentURL: Optional[List[SegmentURLType]] = typic.field(name='SegmentURL', default_factory=list)

    def as_dict(self) -> OrderedDict:
        result = OrderedDict()
        if self.SegmentURL is not None:
            result['@SegmentURL'] = self.SegmentURL.as_dict()
        return result


@typic.klass
class DescriptorType:
    scheme_id_uri: str = typic.field(name='@schemeIdUri')
    value: Optional[str] = typic.field(None, name='@value')
    id: Optional[str] = typic.field(None, name='@id')

    text: Optional[str] = typic.field('')
    children: Optional[OrderedDict] = typic.field(default_factory=OrderedDict)
    other_attrs: Optional[dict] = typic.field(default=dict)

    def as_dict(self) -> OrderedDict:
        result = OrderedDict()
        if self.scheme_id_uri is not None:
            result['@schemeIdUri'] = self.scheme_id_uri
        if self.value is not None:
            result['@value'] = self.value
        if self.id is not None:
            result['@id'] = self.id
        if self.text is not None:
            result['#text'] = self.text
        for k, v in self.children.items():
            result[k] = v
        for k, v in self.other_attrs.items():
            result[f'@{k}'] = v
        return result


@typic.klass
class RepresentationBaseType:
    content_protection: Optional[List[DescriptorType]] = typic.field(name='ContentProtection', default_factory=list)
    audio_channel_configuration: Optional[DescriptorType] = typic.field(None, name='AudioChannelConfiguration')

    profiles: Optional[str] = typic.field(None, name='@profiles')
    width: Optional[int] = typic.field(None, name='@width')
    height: Optional[int] = typic.field(None, name='@height')
    frame_rate: Optional[str] = typic.field(None, name='@frameRate')
    audio_sampling_rate: Optional[str] = typic.field(None, name='@audioSamplingRate')
    mime_type: Optional[str] = typic.field(None, name='@mimeType')
    segment_profiles: Optional[str] = typic.field(None, name='@segmentProfiles')
    codecs: Optional[str] = typic.field(None, name='@codecs')
    maximum_sap_period: Optional[float] = typic.field(None, name='@maximumSAPPeriod')
    start_with_sap: Optional[SAPType] = typic.field(None, name='@startWithSAP')

    def as_dict(self) -> OrderedDict:
        result = OrderedDict()
        if bool(self.content_protection):
            result['ContentProtection'] = []
            for v in self.content_protection:
                result['ContentProtection'].append(v.as_dict())

        if self.audio_channel_configuration is not None:
            result['AudioChannelConfiguration'] = self.audio_channel_configuration.as_dict()
        if self.profiles is not None:
            result['@profiles'] = self.profiles
        if self.width is not None:
            result['@width'] = self.width
        if self.height is not None:
            result['@height'] = self.height
        if self.frame_rate is not None:
            result['@frameRate'] = self.frame_rate
        if self.audio_sampling_rate is not None:
            result['@audioSamplingRate'] = self.audio_sampling_rate
        if self.mime_type is not None:
            result['@mimeType'] = self.mime_type
        if self.segment_profiles is not None:
            result['@segmentProfiles'] = self.segment_profiles
        if self.codecs is not None:
            result['@codecs'] = self.codecs
        if self.maximum_sap_period is not None:
            result['@maximumSAPPeriod'] = self.maximum_sap_period
        if self.start_with_sap is not None:
            result['@startWithSAP'] = self.start_with_sap
        return result


@typic.klass
class SubRepresentationType(RepresentationBaseType):
    level: Optional[int] = typic.field(None, name='@level')
    dependency_level: Optional[int] = typic.field(None, name='@dependencyLevel')
    bandwidth: Optional[int] = typic.field(None, name='@bandwidth')
    content_component: Optional[int] = typic.field(None, name='@contentComponent')

    def as_dict(self) -> OrderedDict:
        result = OrderedDict()
        if self.level is not None:
            result['@level'] = self.level
        if self.dependency_level is not None:
            result['@dependencyLevel'] = self.dependency_level
        if self.bandwidth is not None:
            result['@bandwidth'] = self.bandwidth
        if self.content_component is not None:
            result['@contentComponent'] = self.content_component
        return result


@typic.klass
class RepresentationType(RepresentationBaseType):
    id: Optional[str] = typic.field(None, name='@id')
    bandwidth: Optional[int] = typic.field(None, name='@bandwidth')
    quality_ranking: Optional[int] = typic.field(None, name='@qualityRanking')
    dependency_id:  Optional[str] = typic.field(None, name='@dependencyId')
    media_stream_structure_id:  Optional[str] = typic.field(None, name='@mediaStreamStructureId')

    base_url: Optional[BaseURLType] = typic.field(None, name='BaseURL')
    sub_representation: Optional[SubRepresentationType] = typic.field(None, name='SubRepresentation')
    segment_base: Optional[SegmentBaseType] = typic.field(None, name='SegmentBase')
    segment_b_segment_listase: Optional[SegmentListType] = typic.field(None, name='SegmentList')
    segment_template: Optional[SegmentTemplateType] = typic.field(None, name='SegmentTemplate')

    def as_dict(self) -> OrderedDict:
        result = OrderedDict()
        if self.id is not None:
            result['@id'] = self.id
        if self.bandwidth is not None:
            result['@bandwidth'] = self.bandwidth
        if self.quality_ranking is not None:
            result['@qualityRanking'] = self.quality_ranking
        if self.dependency_id is not None:
            result['@dependencyId'] = self.dependency_id
        if self.media_stream_structure_id is not None:
            result['@mediaStreamStructureId'] = self.media_stream_structure_id
        if self.base_url is not None:
            result['BaseURL'] = self.base_url.as_dict()
        if self.sub_representation is not None:
            result['SubRepresentation'] = self.sub_representation.as_dict()
        if self.segment_base is not None:
            result['SegmentBase'] = self.segment_base.as_dict()
        if self.segment_b_segment_listase is not None:
            result['SegmentList'] = self.segment_b_segment_listase.as_dict()
        if self.segment_template is not None:
            result['SegmentTemplate'] = self.segment_template.as_dict()
        return result


@typic.klass
class AdaptationSetType(RepresentationBaseType):
    base_url: Optional[BaseURLType] = typic.field(None, name='BaseURL')
    segment_base: Optional[SegmentBaseType] = typic.field(None, name='SegmentBase')
    segment_list: Optional[SegmentListType] = typic.field(None, name='SegmentList')
    segment_template: Optional[SegmentTemplateType] = typic.field(None, name='SegmentTemplate')
    representation: Optional[RepresentationType] = typic.field(None, name='Representation')

    id: Optional[int] = typic.field(None, '@id')
    group: Optional[int] = typic.field(None, '@group')
    lang: Optional[str] = typic.field(None, '@lang')
    content_type: Optional[str] = typic.field(None, '@contentType')
    min_bandwidth: Optional[int] = typic.field(None, '@minBandwidth')
    max_bandwidth: Optional[int] = typic.field(None, '@maxBandwidth')
    min_width: Optional[int] = typic.field(None, '@minWidth')
    max_width: Optional[int] = typic.field(None, '@maxWidth')
    min_height: Optional[int] = typic.field(None, '@minHeight')
    max_height: Optional[int] = typic.field(None, '@maxHeight')
    min_frame_rate: Optional[int] = typic.field(None, '@minFrameRate')
    max_frame_rate: Optional[int] = typic.field(None, '@maxFrameRate')
    segment_alignment: Optional[bool] = typic.field(True, '@segmentAlignment')
    subsegment_alignment: Optional[bool] = typic.field(True, '@subsegmentAlignment')
    subsegment_starts_with_sap: Optional[SAPType] = typic.field(0, '@subsegmentStartsWithSAP')

    def as_dict(self) -> OrderedDict:
        result = OrderedDict()
        if self.base_url is not None:
            result['BaseURL'] = self.base_url.as_dict()
        if self.segment_base is not None:
            result['SegmentBase'] = self.segment_base.as_dict()
        if self.segment_list is not None:
            result['SegmentList'] = self.segment_list.as_dict()
        if self.segment_template is not None:
            result['SegmentTemplate'] = self.segment_template.as_dict()
        if self.representation is not None:
            result['Representation'] = self.representation.as_dict()
        if self.id is not None:
            result['@id'] = self.id
        if self.group is not None:
            result['@group'] = self.group
        if self.lang is not None:
            result['@lang'] = self.lang
        if self.content_type is not None:
            result['@contentType'] = self.content_type
        if self.min_bandwidth is not None:
            result['@minBandwidth'] = self.min_bandwidth
        if self.max_bandwidth is not None:
            result['@maxBandwidth'] = self.max_bandwidth
        if self.min_width is not None:
            result['@minWidth'] = self.min_width
        if self.max_width is not None:
            result['@maxWidth'] = self.max_width
        if self.min_height is not None:
            result['@minHeight'] = self.min_height
        if self.max_height is not None:
            result['@maxHeight'] = self.max_height
        if self.min_frame_rate is not None:
            result['@minFrameRate'] = self.min_frame_rate
        if self.max_frame_rate is not None:
            result['@maxFrameRate'] = self.max_frame_rate
        if self.segment_alignment is not None:
            result['@segmentAlignment'] = self.segment_alignment
        if self.subsegment_alignment is not None:
            result['@subsegmentAlignment'] = self.subsegment_alignment
        if self.subsegment_starts_with_sap is not None:
            result['@subsegmentStartsWithSAP'] = self.subsegment_starts_with_sap
        return result


@typic.klass
class PeriodType:
    adaptation_set: Optional[List[AdaptationSetType]] = typic.field(name='AdaptationSet', default_factory=list)

    id: Optional[str] = typic.field(None, '@id')
    start: Optional[DurationType] = typic.field(None, '@start')

    def as_dict(self) -> OrderedDict:
        result = OrderedDict()
        if bool(self.adaptation_set):
            result['AdaptationSet'] = []
            for _as in self.adaptation_set:
                result['AdaptationSet'].append(_as.as_dict())
        if self.id is not None:
            result['@id'] = self.id
        if self.start is not None:
            result['@start'] = self.start
        return result


@typic.klass
class MPD:
    profiles: Optional[str] = typic.field(None, '@profiles')
    min_buffer_time: Optional[DurationType] = typic.field(None, name='@minBufferTime')

    period: Optional[PeriodType] = typic.field(name='Period', default_factory=list)

    type: Optional[Literal['static', 'dynamic']] = typic.field('static', name='@type')
    media_presentation_duration: Optional[DurationType] = typic.field(None, name='@mediaPresentationDuration')

    _addition_attributes: Optional[dict] = typic.field(exclude=True, default_factory=dict)
    _addition_element: Optional[dict] = typic.field(exclude=True, default_factory=dict)

    def as_dict(self) -> OrderedDict:
        result = OrderedDict()
        if self.period is not None:
            result['Period'] = self.period.as_dict()
        if self.profiles is not None:
            result['@profiles'] = self.profiles
        if self.min_buffer_time is not None:
            result['@minBufferTime'] = self.min_buffer_time
        if self.type is not None:
            result['@type'] = self.type
        if self.media_presentation_duration is not None:
            result['@mediaPresentationDuration'] = self.media_presentation_duration
        for k, v in self._addition_attributes.items():
            result[f'@{k}'] = v
        for k, v in self._addition_element.items():
            result[f'{k}'] = v
        return result

    def __str__(self):
        return unparse(self.as_dict())
