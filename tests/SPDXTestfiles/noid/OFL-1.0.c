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
** SPDX License to detect: https://spdx.org/licenses/OFL-1.0.html				
*/



/*
SIL OPEN FONT LICENSE

Version 1.0 - 22 November 2005

PREAMBLE 

The
goals of the Open Font License (OFL) are to stimulate worldwide
development of cooperative font projects, to support the font creation
efforts of academic and linguistic communities, and to provide an open
framework in which fonts may be shared and improved in partnership
with others.

The OFL allows the licensed fonts to be used, studied,
modified and redistributed freely as long as they are not sold by
themselves. The fonts, including any derivative works, can be bundled,
embedded, redistributed and sold with any software provided that the
font names of derivative works are changed. The fonts and derivatives,
however, cannot be released under any other type of
license.

DEFINITIONS 

"Font Software" refers to any and all of the
following:

     - font files 
     - data files 
     - source code 

    - build scripts 
     - documentation 

"Reserved Font Name"
refers to the Font Software name as seen by users and any other names
as specified after the copyright statement.

"Standard Version" refers
to the collection of Font Software components as distributed by the
Copyright Holder.

"Modified Version" refers to any derivative font
software made by adding to, deleting, or substituting — in part or
in whole -- any of the components of the Standard Version, by changing
formats or by porting the Font Software to a new
environment.

"Author" refers to any designer, engineer, programmer,
technical writer or other person who contributed to the Font
Software.

PERMISSION & CONDITIONS 

Permission is hereby granted,
free of charge, to any person obtaining a copy of the Font Software,
to use, study, copy, merge, embed, modify, redistribute, and sell
modified and unmodified copies of the Font Software, subject to the
following conditions:

1) Neither the Font Software nor any of its
individual components, in Standard or Modified Versions, may be sold
by itself.

2) Standard or Modified Versions of the Font Software may
be bundled, redistributed and sold with any software, provided that
each copy contains the above copyright notice and this license. These
can be included either as stand-alone text files, human-readable
headers or in the appropriate machine-readable metadata fields within
text or binary files as long as those fields can be easily viewed by
the user.

3) No Modified Version of the Font Software may use the
Reserved Font Name(s), in part or in whole, unless explicit written
permission is granted by the Copyright Holder. This restriction
applies to all references stored in the Font Software, such as the
font menu name and other font description fields, which are used to
differentiate the font from others.

4) The name(s) of the Copyright
Holder or the Author(s) of the Font Software shall not be used to
promote, endorse or advertise any Modified Version, except to
acknowledge the contribution(s) of the Copyright Holder and the
Author(s) or with their explicit written permission.

5) The Font
Software, modified or unmodified, in part or in whole, must be
distributed using this license, and may not be distributed under any
other license.

TERMINATION 

This license becomes null and void if
any of the above conditions are not met.

DISCLAIMER 

THE FONT
SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO ANY WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT
OF COPYRIGHT, PATENT, TRADEMARK, OR OTHER RIGHT. IN NO EVENT SHALL THE
COPYRIGHT HOLDER BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
INCLUDING ANY GENERAL, SPECIAL, INDIRECT, INCIDENTAL, OR CONSEQUENTIAL
DAMAGES, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF THE USE OR INABILITY TO USE THE FONT SOFTWARE OR FROM
OTHER DEALINGS IN THE FONT SOFTWARE.
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

