using noamChat.Helper.Enums;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace noamChat.Events
{
    public class ThemeEventArgs : EventArgs
    {
        public Theme? NewTheme { get; set; }
    }
}
