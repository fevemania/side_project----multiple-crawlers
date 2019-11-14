FROM fluent/fluentd:v1.4-debian-onbuild-1

USER root

RUN BUILD_DEPS="sudo make gcc g++ libc-dev ruby-dev" \
  && apt-get update \
  && apt-get install -y --no-install-recommends $BUILD_DEPS \
  && apt-get install -y default-libmysqlclient-dev \
  && sudo gem install fluent-plugin-sql mysql2 \
  && fluent-gem install mysql2 --no-document \
  && sudo gem sources --clear-all \
  && SUDO_FORCE_REMOVE=yes \
    apt-get purge -y --auto-remove \
                  -o APT::AutoRemove::RecommendsImportant=false \
                  $BUILD_DEPS \
  && rm -rf /var/lib/apt/lists/* \
           /home/fluent/.gem/ruby/2.3.0/cache/*.gem

COPY ./fluent.conf /fluentd/etc/
USER fluent
