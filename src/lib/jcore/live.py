# -*- coding: utf-8 -*-
import string
import re
from mako.lookup import TemplateLookup
from mako import exceptions

class LiveManager:
    
    STAGE_TMPL      = "stage.tmpl"
    TMPL_SETTING    = {
        'MIC_TMPL'      : "mic.tmpl",
        'AMP_TMPL'      : "amp.tmpl",
        'KEY_TMPL'      : "key.tmpl",
        'OTHER_TMPL'    : "other.tmpl",
        'DRUM_TMPL'     : "drum.tmpl",
        'PERC_TMPL'     : "perc.tmpl",
        'LAINY_TMPL'    : "lainy.tmpl",
        'JC_TMPL'       : "jc.tmpl",
        'AMPEG_TMPL'    : "ampeg.tmpl"
    }

    def __init__(self):
        pass
    
    """
    Create SVG File.
    @param  string params   Live stage setting data.
    @return string          SVG Filename.    
    """
    def create_svg(self, params):
        # load template.
        tmpl_lookup = TemplateLookup(self.tmplate_dir, 
            output_encoding='utf-8', input_encoding='utf-8', default_filters=['decode.utf8'])
        tmpl_stage  = tmpl_lookup.get_template(self.STAGE_TMPL)
        tmpl_params = locals()
        tmpl_params['TMPL_SETTING'] = self.TMPL_SETTING
        del tmpl_params['self']
        return tmpl_stage.render(**tmpl_params)

    def set_template_dir(self, path):
        self.tmplate_dir = path

if __name__ == '__main__':
    params = {}
    params['s_microphone']      = '管:400.95:426.85,normal:328.9:425.85,other:468:425.85'
    params['s_amplifer']        = 'Fender:67:398.8'
    params['s_keyboard']        = 'ZeroOne(01):617.1:433.05'
    params['s_other']           = ''
    params['s_useDrum']         = 'yes'
    params['s_usePercussion']   = 'yes'
    params['s_useLainy']        = 'yes'
    params['s_useJazzCorus']    = 'yes'
    params['s_useAmpeg']        = 'yes'
    lm = LiveManager()
    print lm.create_svg(params)
