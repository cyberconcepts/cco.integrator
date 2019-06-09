'''
Processing Excel files
  
2019-04-28 helmutm@cy55.de
'''

import glob
import os
from os.path import basename, isfile, join
import traceback

from cco.integrator.dispatcher import make_copy


def run_macro(conf, logger):
    source = conf['source_dir']
    fnames = glob.glob(source + '/*')
    for input in fnames:
        if isfile(input):
            fn = basename(input)
            output = join(conf['target_dir'], fn)
            macro = conf.get('macro') or 'main'
            logger.info('run_macro; filename=%s, macro=%s.' % (fn, macro))
            try:
                runExcelMacro(input, output, macro)
            except:
                logger.error(traceback.format_exc())
                make_copy(conf, logger, 'error_dir', input)
            make_copy(conf, logger, 'backup_dir', input)
            os.remove(input)
            return True
    return False


def runExcelMacro(input, output, macro):
    from win32com.client import Dispatch
    myExcel = Dispatch('Excel.Application')
    myExcel.Visible = 0
    myExcel.Workbooks.Add(input)
    myExcel.DisplayAlerts = 0
    myExcel.Run(macro)
    myExcel.ActiveWorkbook.SaveAs(
                output, ReadOnlyRecommended=True, CreateBackup=False)
    myExcel.Quit()
