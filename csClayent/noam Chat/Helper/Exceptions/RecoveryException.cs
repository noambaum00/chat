using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace noamChat.Helper.Exceptions
{
   public class RecoveryException : Exception
    {
        public RecoveryException(string message) : base(message)
        {
        }
    }
}
