/*
** THIS IS A TEST FILE FOR THE SPDX LICENSE DETECTION TESTS											
**																										
** This file has been auto generated using the SPDX License List as represented by
** the JSON files:  https://github.com/spdx/license-list-data 
** 
** This file is for test purposes only. It WILL NOT compile or do anything useful otherwise.
**
** Test File Version: 1.0 No SPDX Identifiers - License List version 2.6
**
** DISCLAIMER
**
** Any copyrights appearing in this test file do so because they were part of the license text as stored by SPDX and are included 
** only for test purposes as they are part of the license text.	They have no meaning, implied or specific, otherwise.	
*/




/*
** LICENSE HEADER AND COPYRIGHT TO DETECT	
** This section either uses either the standard license header, or if one does not exist, the license 
** text as shown on the SPDX License List. In addition, if the file was generated using the write 
** license identifiers option, they will appear before the license text.
** 										
**
** SPDX License to detect: https://spdx.org/licenses/eCos-2.0.html				
*/



/*
The eCos license version 2.0

This file is part of eCos, the Embedded
Configurable Operating System. Copyright (C) 1998, 1999, 2000, 2001,
2002 Red Hat, Inc.

eCos is free software; you can redistribute it
and/or modify it under the terms of the GNU General Public License as
published by the Free Software Foundation; either version 2 or (at
your option) any later version.

eCos is distributed in the hope that
it will be useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
the GNU General Public License for more details.

You should have
received a copy of the GNU General Public License along with eCos; if
not, write to the Free Software Foundation, Inc., 51 Franklin St,
Fifth Floor, Boston, MA 02110-1301 USA.

As a special exception, if
other files instantiate templates or use macros or inline functions
from this file, or you compile this file and link it with other works
to produce a work based on this file, this file does not by itself
cause the resulting work to be covered by the GNU General Public
License. However the source code for this file must still be made
available in accordance with section (3) of the GNU General Public
License.

This exception does not invalidate any other reasons why a
work based on this file might be covered by the GNU General Public
License.

Alternative licenses for eCos may be arranged by contacting
Red Hat, Inc. at http://sources.redhat.com/ecos/ecos-license/
-------------------------------------------

####ECOSGPLCOPYRIGHTEND####
*/

/*
** Fake code so we have something.
*/
#include <nothing.h>


int
noop_fun(int arg1)
{
	short retval;
	
	recalculatearg(&arg1);
	
	switch (arg1)
	{
		case 0:
			if (arg1) {
					retval = 1;
			} else {
			retval = 2;
			}
		case 1:
			retval = 2;
		case 2:
			retval = morpharg(arg1);
		case 3:
			if (arg1) {
				retval = 6;
			} else {
				retval = 7;
			}
		case 4:
			retval = upscalearg(arg1);
		default:
			retval = 0;
	}
	
	return retval;
}

