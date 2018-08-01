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
** SPDX License to detect: https://spdx.org/licenses/SimPL-2.0.html				
*/



/*
Simple Public License (SimPL)

Preamble

This Simple Public License
2.0 (SimPL 2.0 for short) is a plain language implementation of GPL
2.0.  The words are different, but the goal is the same - to guarantee
for all users the freedom to share and change software.  If anyone
wonders about the meaning of the SimPL, they should interpret it as
consistent with GPL 2.0.

Simple Public License (SimPL) 2.0

The SimPL
applies to the software's source and object code and comes with any
rights that I have in it (other than trademarks). You agree to the
SimPL by copying, distributing, or making a derivative work of the
software.

You get the royalty free right to:
     
- Use the software
for any purpose;
- Make derivative works of it (this is called a
"Derived Work");
- Copy and distribute it and any Derived Work.

If
you distribute the software or a Derived Work, you must give back to
the community by:

- Prominently noting the date of any changes you
make;
- Leaving other people's copyright notices, warranty
disclaimers, and license terms  in place;
- Providing the source code,
build scripts, installation scripts, and interface definitions in a
form that is easy to get and best to modify;
- Licensing it to
everyone under SimPL, or substantially similar terms (such as GPL
2.0), without adding further restrictions to the rights provided;
-
Conspicuously announcing that it is available under that
license.

There are some things that you must shoulder:

- You get NO
WARRANTIES. None of any kind;
- If the software damages you in any
way, you may only recover direct damages up to the amount you paid for
it (that is zero if you did not pay anything). You may not recover any
other damages, including those called "consequential damages." (The
state or country where you live may not allow you to limit your
liability in this way, so this may not apply to you);

The SimPL
continues perpetually, except that your license rights end
automatically if:

- You do not abide by the "give back to the
community" terms (your licensees get to keep their rights if they
abide);
- Anyone prevents you from distributing the software under the
terms of the SimPL.

License for the License

You may do anything that
you want with the SimPL text; it's a license form to use in any way
that you find helpful.  To avoid confusion, however, if you change the
terms in any way then you may not call your license the Simple Public
License or the SimPL (but feel free to acknowledge that your license
is "based on the Simple Public License").
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

