using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace noamChat.Events
{
    public class EmojiEventArgs : EventArgs
    {
        public bool ForPrivateChat { get; set; }
        public string EmojiName { get; set; }
    }
}
