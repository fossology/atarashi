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
** SPDX License to detect: https://spdx.org/licenses/Multics.html				
*/



/*
Multics License

Historical Background

This edition of the Multics
software materials and documentation is provided and donated to
Massachusetts Institute of Technology by Group BULL including BULL HN
Information Systems Inc. as a contribution to computer science
knowledge. This donation is made also to give evidence of the common
contributions of Massachusetts Institute of Technology, Bell
Laboratories, General Electric, Honeywell Information Systems Inc.,
Honeywell BULL Inc., Groupe BULL and BULL HN Information Systems Inc.
to the development of this operating system. Multics development was
initiated by Massachusetts Institute of Technology Project MAC
(1963-1970), renamed the MIT Laboratory for Computer Science and
Artificial Intelligence in the mid 1970s, under the leadership of
Professor Fernando Jose Corbato. Users consider that Multics provided
the best software architecture for managing computer hardware properly
and for executing programs. Many subsequent operating systems
incorporated Multics principles. Multics was distributed in 1975 to
2000 by Group Bull in Europe , and in the U.S. by Bull HN Information
Systems Inc., as successor in interest by change in name only to
Honeywell Bull Inc. and Honeywell Information Systems Inc.
.

-----------------------------------------------------------

Permission
to use, copy, modify, and distribute these programs and their
documentation for any purpose and without fee is hereby
granted,provided that the below copyright notice and historical
background appear in all copies and that both the copyright notice and
historical background and this permission notice appear in supporting
documentation, and that the names of MIT, HIS, BULL or BULL HN not be
used in advertising or publicity pertaining to distribution of the
programs without specific prior written permission. 

Copyright 1972
by Massachusetts Institute of Technology and Honeywell Information
Systems Inc. 
Copyright 2006 by BULL HN Information Systems Inc.

Copyright 2006 by Bull SAS All Rights Reserved
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

