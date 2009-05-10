from optparse import OptionParser
import sys
from traceback import print_tb
from prdg.util.emails import EmailIO

class CLIProgram(object):
    """A helper class to write Command Line Interface programs."""
    
    usage = ''
    """An string describing how to use the program."""    
        
    def _configure_parser(self, parser):
        """
        Takes an OptionParser object and add the command line options.                
        
        Arguments:
        parser -- An OptionParser object.
        
        Abstract method.
        """
        pass        
    
    def _check_options_args(self, parser, options, args):
        """
        Check the options and arguments passed in the command line. If an error
        is found then parser.error() is called.
        
        Arguments:
        parser -- An OptionParser object.
        options, args -- As returned by OptionParser.parse_args()        
        
        Abstract method.
        """
        pass
    
    def _do_run(self, options, args, out):
        """
        Execute the program logic.
        
        Arguments:
        options -- An object containing the command line options as attributes.
        args -- Sequence of command line arguments.
        out -- An open file-like where to write the output of the program.
            It must not be closed by this method.
        
        Return: True if and only if the execution was successful.
        
        Raise: Exception if an error occur. (Note: when this method is called
        by run() then the exceptions are automatically included in the 
        output).
        
        Abstract method.
        """
        return True 
       
    def _post_run(self, options, args, out, fail):
        """
        Hook method that is executed after the execution of the program (i.e
        after an invocation of _do_run()).
        
        Arguments:
        options, args -- The program options and args, as returned by 
            parse_args()
        out -- An open file-like where the output of the program was written.
        fail -- A bool indicating whether the program execution was successful
            or not.
            
        Abstract method.
        """
        pass    
    
    def _parse_args(self):
        """
        Parse the command line args and call check_options_args() on it.
        
        Return: a tuple (options, args) as returned by OptionParser.parse_args()
        """
        parser = OptionParser(usage=self.usage)        
        self._configure_parser(parser)
        (options, args) = parser.parse_args()
        self._check_options_args(parser, options, args)
        return (options, args)    
    
    def _get_output(self, options, args):
        """
        Determine where the program output will be written depending on the
        command line options and arguments.
        
        Arguments:
        options, args -- The program options and args, as returned by 
            parse_args()
        
        Return: an open file-like object where the program output will be
        written.
        """
        return sys.stdout
    
    def run(self):
        """Run the program."""
        (options, args) = self._parse_args()
        out = self._get_output(options, args)
        
        fail = True
        try:
            fail = not self._do_run(options, args, out)
        except Exception, e:            
            print >> out, e
            print_tb(sys.exc_info()[2])
        
        self._post_run(options, args, out, fail)
        
        return not fail  
    
class ReportProgram(CLIProgram):
    """
    An structure for programs which generate some output and print it to stdout
    or send it by email. This class handles the command line parsing and sending
    the email (or printing the output).   
    """
    
    def __init__(self, report_name, usage, smtp_server, from_addr):
        """
        Constructor.
        
        Arguments:
        report_name -- The name of the report.
        usage -- An string describing how to use the program.
        """
        CLIProgram.__init__(self, usage)
        
        self.report_name = report_name
        self.smtp_server = smtp_server
        self.from_addr = from_addr
        
    def _configure_parser(self, parser):
        """Override: CLIProgram"""
        parser.add_option('-e', '--email', action='append', dest='emails', 
            help='specify an email where to send the results, can be used'
                ' multiple times')
    
        parser.add_option('-f', '--emailonfailure', action='store_true', 
            dest='email_on_failure_only', default=False, 
            help='send emails only when some site fail')
    
    def _check_options_args(self, parser, options, args):
        """Override: CLIProgram"""
        if options.email_on_failure_only and (not options.emails):
            parser.error('-f/--emailonfailure option does not make sense if an'
                ' email is not specified')
    
    def _get_output(self, options, args):
        """Override: CLIProgram"""
        if options.emails:
            return EmailIO( 
                smtp_server=self.smtp_server, 
                to_addr=options.emails, 
                from_addr=self.from_addr
            )
        
        return CLIProgram._get_output(self, options, args)

    def _post_run(self, options, args, out, fail):
        """Override: CLIProgram"""
        if (options.emails and ((not options.email_on_failure_only) or fail)):            
            if fail:
                out.subject = '%s - FAILED' % self.report_name
            else:
                out.subject = '%s - success' % self.report_name
            
            # Send the email.
            out.close()        
