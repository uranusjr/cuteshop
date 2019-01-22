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
{%- for target_name, dir in public_header_dirs %}
{{ target_name }}.target = ../../include/{{ name }}/{{ dir }}
{{ target_name }}.commands = \
    $$MKDIR $$system_path(../../include/{{ name }}/{{ dir }})
{%- endfor %}
public_header_dirs.depends = \
    {%- for target_name, dir in public_header_dirs %}
    {{ target_name }}{%- if not loop.last %} \{% endif %}
    {%- endfor %}
{%- for target_name, source, target in public_headers %}
{{ target_name }}.depends = public_header_dirs
{{ target_name }}.target = ../../include/{{ name }}/{{ target }}
{{ target_name }}.commands = \
    $(COPY_FILE) \"$$shell_path($$PWD/{{ source }})\" \
    \"$$shell_path(../../include/{{ name }}/{{ target }})\"
{%- endfor %}
public_headers.depends = \
    {%- for target_name, _, _ in public_headers %}
    {{ target_name }} \
    {%- endfor %}
    public_header_dirs
QMAKE_EXTRA_TARGETS += \
    {%- for target_name, _, _ in public_headers %}
    {{ target_name }} \
    {%- endfor %}
    {%- for target_name, _ in public_header_dirs %}
    {{ target_name }} \
    {%- endfor %}
    public_header_dirs \
    public_headers
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
