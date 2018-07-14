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
** SPDX License to detect: https://spdx.org/licenses/DOC.html				
*/



/*
Copyright and Licensing Information for ACE(TM), TAO(TM), CIAO(TM),
DAnCE(TM), and CoSMIC(TM)

ACE(TM), TAO(TM), CIAO(TM), DAnCE>(TM), and
CoSMIC(TM) (henceforth referred to as "DOC software") are copyrighted
by Douglas C. Schmidt and his research group at Washington University,
University of California, Irvine, and Vanderbilt University, Copyright
(c) 1993-2009, all rights reserved. Since DOC software is open-source,
freely available software, you are free to use, modify, copy, and
distribute--perpetually and irrevocably--the DOC software source code
and object code produced from the source, as well as copy and
distribute modified versions of this software. You must, however,
include this copyright statement along with any code built using DOC
software that you release. No copyright statement needs to be provided
if you just ship binary executables of your software products.

You
can use DOC software in commercial and/or binary software releases and
are under no obligation to redistribute any of your source code that
is built using DOC software. Note, however, that you may not
misappropriate the DOC software code, such as copyrighting it yourself
or claiming authorship of the DOC software code, in a way that will
prevent DOC software from being distributed freely using an
open-source development model. You needn't inform anyone that you're
using DOC software in your software, though we encourage you to let us
know so we can promote your project in the DOC software success
stories.

The ACE, TAO, CIAO, DAnCE, and CoSMIC web sites are
maintained by the DOC Group at the Institute for Software Integrated
Systems (ISIS) and the Center for Distributed Object Computing of
Washington University, St. Louis for the development of open-source
software as part of the open-source software community. Submissions
are provided by the submitter ``as is'' with no warranties whatsoever,
including any warranty of merchantability, noninfringement of third
party intellectual property, or fitness for any particular purpose. In
no event shall the submitter be liable for any direct, indirect,
special, exemplary, punitive, or consequential damages, including
without limitation, lost profits, even if advised of the possibility
of such damages. Likewise, DOC software is provided as is with no
warranties of any kind, including the warranties of design,
merchantability, and fitness for a particular purpose,
noninfringement, or arising from a course of dealing, usage or trade
practice. Washington University, UC Irvine, Vanderbilt University,
their employees, and students shall have no liability with respect to
the infringement of copyrights, trade secrets or any patents by DOC
software or any part thereof. Moreover, in no event will Washington
University, UC Irvine, or Vanderbilt University, their employees, or
students be liable for any lost revenue or profits or other special,
indirect and consequential damages.

DOC software is provided with no
support and without any obligation on the part of Washington
University, UC Irvine, Vanderbilt University, their employees, or
students to assist in its use, correction, modification, or
enhancement. A number of companies around the world provide commercial
support for DOC software, however. DOC software is Y2K-compliant, as
long as the underlying OS platform is Y2K-compliant. Likewise, DOC
software is compliant with the new US daylight savings rule passed by
Congress as "The Energy Policy Act of 2005," which established new
daylight savings times (DST) rules for the United States that expand
DST as of March 2007. Since DOC software obtains time/date and
calendaring information from operating systems users will not be
affected by the new DST rules as long as they upgrade their operating
systems accordingly.

The names ACE(TM), TAO(TM), CIAO(TM), DAnCE(TM),
CoSMIC(TM), Washington University, UC Irvine, and Vanderbilt
University, may not be used to endorse or promote products or services
derived from this source without express written permission from
Washington University, UC Irvine, or Vanderbilt University. This
license grants no permission to call products or services derived from
this source ACE(TM), TAO(TM), CIAO(TM), DAnCE(TM), or CoSMIC(TM), nor
does it grant permission for the name Washington University, UC
Irvine, or Vanderbilt University to appear in their names.

If you
have any suggestions, additions, comments, or questions, please let me
know.

Douglas C. Schmidt

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

