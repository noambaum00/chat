using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Collections.ObjectModel;
using noamChat.ViewModels;

namespace noamChat.Events
{
    public class ConnectionEventArgs : EventArgs
    {
        public ChatViewModel ChatViewModelContext;
    }
}
