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
** SPDX License to detect: https://spdx.org/licenses/psutils.html				
*/



/* SPDX-License-Identifier: psutils */
/*
PS Utilities Package

The constituent files of this package listed
below are copyright (C) 1991-1995 Angus J. C. Duggan.

LICENSE        
 Makefile.msc     Makefile.nt	   Makefile.os2
Makefile.unix    README 
         config.h         descrip.mms
epsffit.c        epsffit.man	 
extractres.man   extractres.pl
fixdlsrps.man    fixdlsrps.pl    
fixfmps.man	   fixfmps.pl
fixmacps.man     fixmacps.pl	 
fixpsditps.man   fixpsditps.pl
fixpspps.man     fixpspps.pl	 
fixscribeps.man  fixscribeps.pl
fixtpps.man	 fixtpps.pl	  fixwfwps.man
    fixwfwps.pl
fixwpps.man	 fixwpps.pl	  fixwwps.man	  
fixwwps.pl
getafm           getafm.man	  includeres.man  
includeres.pl
maketext         patchlev.h	  psbook.c        
psbook.man
pserror.c        pserror.h        psmerge.man	  
psmerge.pl
psnup.c          psnup.man        psresize.c	  
psresize.man
psselect.c	 psselect.man     psspec.c        
psspec.h
pstops.c         pstops.man	  psutil.c        
psutil.h
showchar

They may be copied and used for any purpose
(including distribution as part of a for-profit product),
provided:

1) The original attribution of the programs is clearly
displayed in the product and/or documentation, even if the programs
are modified and/or renamed as part of the product.

2) The original
source code of the programs is provided free of charge (except for
reasonable distribution costs). For a definition of reasonable
distribution costs, see the Gnu General Public License or Larry Wall's
Artistic License (provided with the Perl 4 kit). The GPL and Artistic
License in NO WAY affect this license; they are merely used as
examples of the spirit in which it is intended.

3) These programs are
provided "as-is". No warranty or guarantee of their fitness for any
particular task is provided. Use of these programs is completely at
your own risk.

Basically, I don't mind how you use the programs so
long as you acknowledge the author, and give people the originals if
they want them.
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

