﻿using noamChat.Helper.Enums;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace noamChat.Models
{
    public class LogModel
    {
        public string Message { get; }
        public LogModel(string message) => Message = message;
    }
}
