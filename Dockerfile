# Atarashi Dockerfile
# Copyright (C) 2018-2019 Gaurav Mishra, mishra.gaurav@siemens.com
#
# This package is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 dated June, 1991.
#
# This package is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this package; if not, write to the Free Software Foundation,
# Inc., 51 Franklin St, Fifth Floor, Boston,
# MA 02110-1301, USA.
#
# Description: Docker container image recipe

FROM python:3.7 as builder

WORKDIR /atarashi

COPY . .

RUN mkdir wheels
RUN python -m pip wheel --use-pep517 --wheel-dir wheels .

FROM python:3.7-slim

LABEL maintainer="Fossology <fossology@fossology.org>"
LABEL Description="Image for Atarashi project"

RUN useradd --create-home atarashi

WORKDIR /home/atarashi

COPY --from=builder /atarashi/wheels/ .

RUN python -m pip install ./*.whl \
 && rm ./*.whl

USER atarashi

ENTRYPOINT ["atarashi"]
CMD ["-h"]
