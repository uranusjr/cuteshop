include(../../common.pri)

QT = {{ ' '.join(qt) }}

TARGET = {{ target }}

# Disable all warnings.
{#- TODO: Make it configurable #}
QMAKE_CFLAGS_WARN_ON =

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
public_headers_dir.commands = $$MKDIR $$system_path(../../include/{{ name }})
public_headers_dir.target = ../../include/{{ name }}
public_headers.commands = \
    {%- for f in public_headers %}
    $(COPY_FILE) $$shell_path($$PWD/{{ f }}) \
    $$shell_path(../../include/{{ name }})
    {%- if not loop.last %} && \{% endif %}
    {%- endfor %}
public_headers.depends = public_headers_dir
QMAKE_EXTRA_TARGETS += public_headers_dir public_headers
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
{%- if extra %}

{{ extra }}

{%- endif -%}
