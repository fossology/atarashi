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
** SPDX License to detect: https://spdx.org/licenses/CrystalStacker.html				
*/



/*
Crystal Stacker is freeware. This means you can pass copies around
freely provided you include this document in it's original form in
your distribution. Please see the "Contacting Us" section of this
document if you need to contact us for any
reason.

Disclaimer

NewCreature Design makes no guarantees regarding
the Crystal Stacker software. We are not responsible for damages
caused by it, though the software is not known to cause any problems.
If you have trouble with the software, see the "Contacting Us" section
of this document.

The source code is provided as-is and you may do
with it whatsoever you please provided that you include this file in
its unmodified form with any new distribution. NewCreature Design
makes no gaurantees regarding the usability of the source but are
willing to help with any problems you might run into. Please see the
"Contacting Us" section of this document if you need to get in touch
with us about any issues you have regarding the source.
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

