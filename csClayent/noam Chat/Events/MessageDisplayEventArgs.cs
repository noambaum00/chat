using System;
using noamChat.Helper.Enums;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace noamChat.Events
{
    public class MessageDisplayEventArgs : EventArgs
    {
        public MessageDisplay? NewMessageDisplay { get; set; }
    }
}
