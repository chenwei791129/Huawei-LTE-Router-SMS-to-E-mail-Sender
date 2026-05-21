#
# Dockerfile for awei/huawei-lte-router-sms-to-email-sender
#

FROM ghcr.io/astral-sh/uv:python3.14-alpine
LABEL MAINTAINER AwEi

ENV HUAWEI_ROUTER_IP_ADDRESS=192.168.8.1 \
    HUAWEI_ROUTER_ACCOUNT=admin \
    DELAY_SECOND=10 \
    LOCALE=en_US

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# Install dependencies first for better layer caching
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

COPY check-sms.py ./
COPY locale ./locale

# Drop .pot template files — only the compiled .mo are needed at runtime
RUN rm -f /app/locale/en/LC_MESSAGES/messages.pot \
          /app/locale/en_US/LC_MESSAGES/messages.pot \
          /app/locale/zh_CN/LC_MESSAGES/messages.pot \
          /app/locale/zh_HK/LC_MESSAGES/messages.pot \
          /app/locale/zh_TW/LC_MESSAGES/messages.pot

ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "check-sms.py"]
