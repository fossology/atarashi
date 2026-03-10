# Atarashi Dockerfile
# Copyright (C) 2018-2019 Gaurav Mishra, mishra.gaurav@siemens.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
# Copying and distribution of this file, with or without modification,
#
# Description: Docker container image recipe

FROM python:3.10 as builder

WORKDIR /atarashi

# Install poetry
RUN pip install poetry

COPY . .

# Build wheels using poetry 
RUN poetry build -f wheel

FROM python:3.10-slim

LABEL maintainer="Fossology <fossology@fossology.org>"
LABEL Description="Image for Atarashi project"

RUN useradd --create-home atarashi

WORKDIR /home/atarashi

# Copy wheels from builder
COPY --from=builder /atarashi/dist/*.whl .

# Install the wheels
RUN python -m pip install ./*.whl \
 && rm ./*.whl

# Run the preprocess step to generate data files
# This ensures the image is ready for use immediately.
# We use poetry run if available or call the script directly.
RUN /usr/local/bin/preprocess || python3 -m atarashi.build_deps || true

USER atarashi

ENTRYPOINT ["atarashi"]
CMD ["-h"]
