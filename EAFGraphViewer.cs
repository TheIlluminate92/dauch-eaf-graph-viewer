// Small Windows entry point: owns the private local viewer process and accepts RPH drops.
// Plotting and view editing open in the user's browser; no external server is used.
using System;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

public class GraphViewer : Form {
    Label status = new Label();
    Button choose = new Button(), open = new Button();
    Process engine;
    string url;
    bool busy;
    public GraphViewer(string[] args) {
        Text="Dauch | EAF Graph Viewer";Size=new Size(740,440);MinimumSize=new Size(620,400);
        StartPosition=FormStartPosition.CenterScreen;BackColor=Color.FromArgb(244,245,247);Font=new Font("Segoe UI",11);
        var heading=new Label {Text="DAUCH  /  EAF GRAPH VIEWER",Dock=DockStyle.Top,Height=90,TextAlign=ContentAlignment.MiddleCenter,
            BackColor=Color.FromArgb(37,41,46),ForeColor=Color.White,Font=new Font("Segoe UI",22,FontStyle.Bold)};
        Controls.Add(heading);
        var body=new FlowLayoutPanel {Dock=DockStyle.Fill,Padding=new Padding(25),FlowDirection=FlowDirection.TopDown,WrapContents=false,AutoScroll=true};
        Controls.Add(body);body.BringToFront();
        var drop=new Label {Text="Drop RPH recordings here",Height=80,Width=650,AllowDrop=true,BackColor=Color.White,
            ForeColor=Color.FromArgb(200,16,46),TextAlign=ContentAlignment.MiddleCenter,Font=new Font("Segoe UI",20,FontStyle.Bold)};
        body.Controls.Add(drop);
        body.Controls.Add(new Label {Text="Five starter views. Compare heats or cycle through them.",AutoSize=true,Margin=new Padding(0,12,0,12)});
        var buttons=new FlowLayoutPanel {Width=650,Height=50};
        choose.Text="Add RPH files";choose.Size=new Size(190,42);choose.BackColor=Color.FromArgb(200,16,46);choose.ForeColor=Color.White;choose.FlatStyle=FlatStyle.Flat;
        open.Text="Open graph viewer";open.Size=new Size(200,42);open.Enabled=false;buttons.Controls.Add(choose);buttons.Controls.Add(open);body.Controls.Add(buttons);
        status.Size=new Size(650,75);status.Text="Starting viewer...";body.Controls.Add(status);
        body.Resize+=(s,e)=>{drop.Width=Math.Max(400,body.ClientSize.Width-60);status.Width=drop.Width;};
        choose.Click+=(s,e)=>{using(var d=new OpenFileDialog {Filter="RPH recordings (*.rph)|*.rph",Multiselect=true})if(d.ShowDialog()==DialogResult.OK)LoadFiles(d.FileNames);};
        open.Click+=(s,e)=>OpenViewer();
        DragEventHandler enter=(s,e)=>e.Effect=!busy&&url!=null&&e.Data.GetDataPresent(DataFormats.FileDrop)?DragDropEffects.Copy:DragDropEffects.None;
        DragEventHandler dropped=(s,e)=>{if(e.Data.GetDataPresent(DataFormats.FileDrop))LoadFiles((string[])e.Data.GetData(DataFormats.FileDrop));};
        AllowDrop=true;DragEnter+=enter;DragDrop+=dropped;drop.DragEnter+=enter;drop.DragDrop+=dropped;
        Shown+=async(s,e)=>{
            busy=true;choose.Enabled=false;
            try {
                var info=new ProcessStartInfo(Path.Combine(AppDomain.CurrentDomain.BaseDirectory,"engine","EAFGraphEngine.exe"),"--no-browser"){
                    UseShellExecute=false,CreateNoWindow=true,RedirectStandardOutput=true,RedirectStandardError=true,StandardOutputEncoding=Encoding.UTF8,StandardErrorEncoding=Encoding.UTF8};
                engine=Process.Start(info);
                var errors=engine.StandardError.ReadToEndAsync();
                var firstLine=engine.StandardOutput.ReadLineAsync();
                if(await Task.WhenAny(firstLine,Task.Delay(30000))!=firstLine)throw new Exception("The viewer took too long to start.");
                url=await firstLine;
                Uri parsed;
                if(!Uri.TryCreate(url,UriKind.Absolute,out parsed)||parsed.Host!="127.0.0.1")throw new Exception("The viewer did not start. "+(engine.HasExited?await errors:""));
                status.Text="Ready. Keep this window open while using the viewer.\nYour saved views remain available after closing.";open.Enabled=true;
            }catch(Exception ex){url=null;open.Enabled=false;try{if(engine!=null&&!engine.HasExited)engine.Kill();}catch(InvalidOperationException){}status.Text="Could not start the graph viewer.";MessageBox.Show(this,ex.Message,"Viewer startup");}
            finally{busy=false;choose.Enabled=url!=null;}
            if(url!=null){if(args.Length>0)LoadFiles(args);else OpenViewer();}
        };
        // Terminate only the service created by this window, never another viewer session.
        FormClosed+=(s,e)=>{try{if(engine!=null&&!engine.HasExited)engine.Kill();}catch(InvalidOperationException){}finally{if(engine!=null)engine.Dispose();}};
        FormClosing+=(s,e)=>{if(busy){e.Cancel=true;status.Text="Please wait for file loading to finish.";}};
    }
    async void OpenViewer(){try{await Task.Run(()=>Process.Start(new ProcessStartInfo(url){UseShellExecute=true}));}catch(Exception e){MessageBox.Show(this,e.Message,"Open viewer");}}
    async void LoadFiles(string[] files){
        if(busy||url==null)return;
        if(files.Length==0||files.Any(f=>!File.Exists(f)||!f.EndsWith(".rph",StringComparison.OrdinalIgnoreCase))){MessageBox.Show(this,"Choose existing RPH files.");return;}
        busy=true;choose.Enabled=false;status.Text="Loading "+files.Length+" recording(s)...";
        try{
            await Task.Run(()=>{foreach(var file in files){
                var info=new FileInfo(file);if(info.Length>128L*1024*1024)throw new Exception(info.Name+" exceeds 128 MB.");
                var request=(HttpWebRequest)WebRequest.Create(url+"upload?name="+Uri.EscapeDataString(info.Name));
                request.Method="POST";request.ContentType="application/octet-stream";request.ContentLength=info.Length;request.Timeout=120000;
                request.Proxy=null;request.ReadWriteTimeout=120000;
                using(var stream=request.GetRequestStream())using(var source=File.OpenRead(file))source.CopyTo(stream);
                try{using(var response=request.GetResponse()){} }
                catch(WebException ex){if(ex.Response==null)throw;using(var response=ex.Response)using(var reader=new StreamReader(response.GetResponseStream()))throw new Exception(info.Name+": "+reader.ReadToEnd());}
            }});
            status.Text="Recordings loaded. Use Overlay files to compare, or Previous / Next to cycle.";OpenViewer();
        }catch(Exception ex){status.Text="Some recordings could not load. Valid files already added remain available.";MessageBox.Show(this,ex.Message,"Unable to load recording");}
        finally{busy=false;choose.Enabled=true;}
    }
    [STAThread]public static void Main(string[] args){Application.EnableVisualStyles();Application.SetCompatibleTextRenderingDefault(false);Application.Run(new GraphViewer(args));}
}
