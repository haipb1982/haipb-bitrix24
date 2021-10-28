

def HaravanToBitrix24(ha):
    bx = {}
    
    bx['ID'] = 999 #???
    bx['TITLE'] = ha.line_items

    return bx


def Bitrix24ToHaravan(bx):
    ha = {}
    
    ha['id'] = 999 #???
    ha['name'] = bx.TITLE

    return ha
