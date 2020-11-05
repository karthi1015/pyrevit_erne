import os
import os.path as op
import shutil

current_dir = op.dirname(__file__)
icon_name = "icon.png"
icon_path = op.join(op.dirname(current_dir), icon_name)
extension_path = op.dirname(op.dirname(op.dirname(op.dirname(op.dirname(current_dir)))))
script_path = "sandbox.extension/pyRevitERNE.tab/Sandbox.panel/Sandbox.pulldown/HelloSandbox.pushbutton"
script_template_name = "sandbox_template.py"
script_final_name = "HelloSandbox_script.py"
script_source_path = op.join(current_dir, script_template_name)
target_path = op.join(extension_path, script_path)
script_target_path = op.join(target_path, script_final_name)
icon_target_path = op.join(op.dirname(target_path), icon_name)

if not op.exists(target_path):
    os.makedirs(target_path)
    shutil.copy(icon_path, icon_target_path)
    shutil.copy(script_source_path, script_target_path)

    print("following directory created:")
    print("  {}".format(target_path))
    print("following files created:")
    print("  {}".format(icon_target_path))
    print("  {}".format(script_target_path))
    print("pyRevit sand box created - happy hacking! (-;")
    print("after revit reload/restart you should see a ")
    print("Sandbox button appear in pyRevitERNE")

else:
    print("pyRevit sandbox seems to be already created - exiting.")
