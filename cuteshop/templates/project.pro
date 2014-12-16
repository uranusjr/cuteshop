include(../../common.pri)

QT = {{ ' '.join(qt) }}

TARGET = {{ name }}

# Disable all warnings.
# TODO: Make it configurable
QMAKE_CFLAGS_WARN_ON =

{% if public_headers -%}
# Header installations.
public_headers_dir.commands = $$MKDIR ../../include/{{ name }}
public_headers_dir.target = ../../include/{{ name }}
public_headers.commands = \
    $$COPY \
    {%- for f in public_headers %}
    {{ f }} \
    {%- endfor %}
    ../../include/{{ name }}
public_headers.depends = public_headers_dir
QMAKE_EXTRA_TARGETS += public_headers_dir public_headers
POST_TARGETDEPS += public_headers
{%- endif %}

{% if sources -%}
SOURCES += \
    {%- for f in sources %}
    {{ f }}{% if not loop.last %} \{% endif %}
    {%- endfor %}
{%- endif %}

{% if headers -%}
HEADERS += \
    {%- for f in headers %}
    {{ f }}{% if not loop.last %} \{% endif %}
    {%- endfor %}
{%- endif %}
