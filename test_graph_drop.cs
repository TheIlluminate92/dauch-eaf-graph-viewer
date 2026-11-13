// Automated WinForms drop integration against the actual packaged launcher assembly.
// This dispatches Windows Forms drop events; it is not a physical mouse-drag test.
using System;
using System.IO;
using System.Net;
using System.Reflection;
using System.Windows.Forms;
class DropCheck {
    [STAThread] static int Main(string[] args) {
        Environment.SetEnvironmentVariable("LOCALAPPDATA",Path.GetFullPath(args[1]));
        var assembly=Assembly.LoadFrom(Path.GetFullPath(args[0]));
        var type=assembly.GetType("GraphViewer");
        var form=(Form)Activator.CreateInstance(type,new object[]{new string[0]});
        var flags=BindingFlags.NonPublic|BindingFlags.Instance;
        var timer=new Timer {Interval=250};bool dropped=false,passed=false;int ticks=0;
        timer.Tick+=(s,e)=>{
            if(++ticks>160){timer.Stop();Console.WriteLine("FAIL: launcher/drop timed out");Environment.Exit(1);}
            var url=(string)type.GetField("url",flags).GetValue(form);
            var busy=(bool)type.GetField("busy",flags).GetValue(form);
            if(url==null||busy)return;
            if(!dropped){
                var paths=new string[args.Length-2];Array.Copy(args,2,paths,0,paths.Length);
                var data=new DataObject(DataFormats.FileDrop,paths);
                var ev=new DragEventArgs(data,0,0,0,DragDropEffects.Copy,DragDropEffects.None);
                typeof(Control).GetMethod("OnDragEnter",flags).Invoke(form,new object[]{ev});
                if(ev.Effect!=DragDropEffects.Copy)throw new Exception("Drop rejected");
                typeof(Control).GetMethod("OnDragDrop",flags).Invoke(form,new object[]{ev});dropped=true;return;
            }
            using(var client=new WebClient()){
                string state=client.DownloadString(url+"state");
                if(System.Text.RegularExpressions.Regex.Matches(state,"\"rows\"\\s*:").Count!=args.Length-2)throw new Exception("Not all dropped recordings were loaded");
            }
            if(!((Button)type.GetField("choose",flags).GetValue(form)).Enabled)throw new Exception("File picker stayed disabled");
            passed=true;timer.Stop();form.Close();
        };
        timer.Start();Application.Run(form);Console.WriteLine(passed?"PASS: packaged launcher starts engine, accepts six-file drop, uploads files, and re-enables selection.":"FAIL");return passed?0:1;
    }
}
