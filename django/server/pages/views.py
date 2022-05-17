# Copyright The OpenTelemetry Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from django.http import HttpResponse
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
)

endpoint_ip = os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT', 'host.docker.internal:9095')
resource = Resource.create({
    "service.name": "django-server-demo-tracer",
    "prcoess.uuid": "550e8400-e29b-41d4-a716-446655440000"
})

otlp_exporter = OTLPSpanExporter(
    endpoint=endpoint_ip,
    insecure=True)

tracer_provider = TracerProvider()
trace.set_tracer_provider(tracer_provider)
tracer = trace.get_tracer_provider().get_tracer(__name__)

span_processor_otlp = BatchSpanProcessor(otlp_exporter)
tracer_provider.add_span_processor(span_processor_otlp)


def home_page_view(request):
    with tracer.start_as_current_span("client"):
        return HttpResponse("Hello, world")
