include(../../common.pri)

TEMPLATE = {{ template }}

{%- if template == 'lib' %}

CONFIG += staticlib

QT = {{ ' '.join(qt) }}

TARGET = {{ target }}

# Disable all warnings.
{#- TODO: Make it configurable #}
QMAKE_CFLAGS_WARN_ON =

{%- endif %}
{%- if config %}

CONFIG += \
    {{ ' \\\n    '.join(config) }}

{%- endif %}
{%- if defines %}

DEFINES += \
    {{ ' \\\n    '.join(defines) }}

{%- endif %}
{%- if includepath %}

INCLUDEPATH += \
    {{ ' \\\n    '.join(includepath) }}

{%- endif %}
{%- if public_headers %}

# Header installations.
public_headers.commands = \
    {%- for dir in public_header_dirs %}
    $$MKDIR $$system_path(../../include/{{ name }}/{{ dir }}) && \
    {%- endfor %}
    {%- for source, target in public_headers %}
    $(COPY_FILE) \"$$shell_path($$PWD/{{ source }})\" \
    \"$$shell_path(../../include/{{ name }}/{{ target }})\"
    {%- if not loop.last %} && \{% endif %}
    {%- endfor %}
QMAKE_EXTRA_TARGETS += public_headers
POST_TARGETDEPS += public_headers

{%- endif %}
{%- if sources %}

SOURCES += \
    {{ ' \\\n    '.join(sources) }}

{%- endif %}
{%- if headers %}

HEADERS += \
    {{ ' \\\n    '.join(headers) }}

{%- endif %}
{%- if forms %}

FORMS += \
    {{ ' \\\n    '.join(forms) }}

{%- endif %}
{%- if resources %}

RESOURCES += \
    {{ ' \\\n    '.join(resources) }}

{%- endif %}
{%- if other_files %}

OTHER_FILES += \
    {{ ' \\\n    '.join(other_files) }}

{%- endif %}
{%- if extra %}

{{ extra }}

{%- endif -%}
