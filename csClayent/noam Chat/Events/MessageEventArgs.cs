using noamChat.Helper.Enums;
using noamChat.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace noamChat.Events
{
    public class MessageEventArgs
    {
        public MessageModel MessageModel { get; set; }
        public Theme? CurrentTheme { get; set; }
    }
}
