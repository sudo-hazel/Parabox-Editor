headers = {
    "hue_shift": {"default": 0}, "ice_move": {"default": 0}, "white_eyes": {"default": 0},
    "seam_fix": {"default": 1}, "banish_fix": {"default": 1}, "epsi_fix": {"default": 0}, "ifzeat_fix": {"default": 0},
    "zoom_out": {"default": 0}, "zoom_in": {"default": 0},
    "winfz_sensitivity": {"default": 0 }
}
tags = {
    "base": ["IFZ","PCF","AIE","PIN","ANT","NOV","LSH","LIP","WEI"],
    # WARNING: LSH and LIP are short functioning
    "short": ["NLR","WRP","AUT"],
    "long": ["LAO"]
}
def savekeys(rb,indent):
        ret = ""
        for key in rb.usefulTags:
            if key in ["LSH", "LIP"]:
                 ret += "\n" + "\t"*indent + "?" + key + " 1"
            else:
                ret += "\n" + "\t"*indent + "?" + key 
        for key in rb.usefulVal:
            ret += "\n" + "\t"*indent + "?" + key + " " + str(rb.usefulVal[key])
        return ret
def tagchange1(rb, tag, value):
    if value:
        rb.usefulTags.append(tag)
    else:
        rb.usefulTags.remove(tag) 
def umenu(rb,imgui):
            if imgui.begin_menu("UsefulMod"):
                imgui.begin_group()
                ###

                changed, value = imgui.checkbox("Camera Follow", "PCF" in rb.usefulTags)
                if changed:
                    tagchange1(rb, "PCF", bool(value))
                
                changed, value = imgui.checkbox("NOV(!)", "NOV" in rb.usefulTags)
                if changed:
                    tagchange1(rb, "NOV", bool(value))

                changed, value = imgui.checkbox("Inf Zone", "IFZ" in rb.usefulTags)
                if changed:
                    tagchange1(rb, "IFZ", bool(value))

                changed, value = imgui.checkbox("Weighted", "WEI" in rb.usefulTags)
                if changed:
                    tagchange1(rb, "WEI", bool(value))

                changed, value = imgui.checkbox("Anti", "ANT" in rb.usefulTags)
                if changed:
                    tagchange1(rb, "ANT", bool(value))

                changed, value = imgui.checkbox("Pinned", "PIN" in rb.usefulTags)
                if changed:
                    tagchange1(rb, "PIN", bool(value))

                changed, value = imgui.checkbox("Enter Inf", "AIE" in rb.usefulTags)
                if changed:
                    tagchange1(rb, "AIE", bool(value))
                imgui.end_group()
                ###
                imgui.same_line()
                ###
                # Hack a separator in
                imgui.begin_group()
                text_val = ""
                imgui.input_text_multiline('',text_val,2056, width=1 )
                imgui.end_group()
                ###
                imgui.same_line()
                imgui.begin_group()
                if rb.player:
                    imgui.text("Auto:")
                    aut = -1
                    if "AUT" in rb.usefulVal:
                        aut = int(rb.usefulVal["AUT"])
                    if imgui.radio_button("U", aut == 0):
                        if aut == -1:
                            rb.usefulVal["AUT"] = 0
                        else:
                            del rb.usefulVal["AUT"]
                    imgui.same_line()
                    if imgui.radio_button("D", aut == 1):
                        if aut == -1:
                            rb.usefulVal["AUT"] = 1
                        else:
                            del rb.usefulVal["AUT"]
                    imgui.same_line()
                    if imgui.radio_button("L", aut == 2):
                        if aut == -1:
                            rb.usefulVal["AUT"] = 2
                        else:
                            del rb.usefulVal["AUT"]
                    imgui.same_line()
                    if imgui.radio_button("R", aut == 3):
                        if aut == -1:
                            rb.usefulVal["AUT"] = 3
                        else:
                            del rb.usefulVal["AUT"]
                changed, value = imgui.checkbox("NLR", "NLR" in rb.usefulVal)
                if changed:
                    if value:#==True
                        rb.usefulVal["NLR"]=0
                    else: del rb.usefulVal["NLR"]
                nlrid = 0
                if "NLR" in rb.usefulVal: nlrid = rb.usefulVal["NLR"]
                imgui.core.push_item_width(120)
                changed, int_val = imgui.input_int('ID', nlrid)
                imgui.core.pop_item_width()
                imgui.end_group()
                ##
                imgui.end_menu()
                
            # This should only work for blocks 
            if hasattr(rb, "refs"):
                if imgui.begin_menu("Useful2"):
                
                    imgui.text("Wrap:")
                    wrp = 0
                    if "WRP" in rb.usefulVal:
                        wrp = int(rb.usefulVal["WRP"])
                    # Bitwise Pain
                    changed, value = imgui.checkbox("U", (wrp & 1)==1)
                    if changed: rb.usefulVal["WRP"]= wrp ^ 1
                    imgui.same_line()
                    changed, value = imgui.checkbox("D", wrp & 2)
                    if changed: rb.usefulVal["WRP"]= wrp ^ 2
                    imgui.same_line()
                    changed, value = imgui.checkbox("L", wrp & 4)
                    if changed: rb.usefulVal["WRP"]= wrp ^ 4
                    imgui.same_line()
                    changed, value = imgui.checkbox("R", wrp & 8)
                    if changed: rb.usefulVal["WRP"]= wrp ^ 8
                    # End bitwise pain
                    if "WRP" in rb.usefulVal and rb.usefulVal["WRP"]==0:
                        del rb.usefulVal["WRP"]
                    changed, value = imgui.checkbox("Shed", "LSH" in rb.usefulTags)
                    if changed: tagchange1(rb, "LSH", bool(value))
                    imgui.same_line()
                    changed, value = imgui.checkbox("Inner Push", "LIP" in rb.usefulTags)
                    if changed: tagchange1(rb, "LIP", bool(value))
                    if imgui.begin_menu("Local Priority"):
                        # get priority order
                        enabled_moves=['push','enter','eat','possess']
                        if "LAO" in rb.usefulVal:
                            enabled_moves = rb.usefulVal["LAO"].split(",")
                        disabled_moves=[move for move in ['push','enter','eat','possess'] if move not in enabled_moves]
                        for i, item in enumerate(enabled_moves):
                            if imgui.arrow_button(item + "-uu", imgui.DIRECTION_UP) and i != 0:
                                enabled_moves[i], enabled_moves[i-1] = enabled_moves[i-1], enabled_moves[i]
                            imgui.same_line()
                            if imgui.arrow_button(item + "-du", imgui.DIRECTION_DOWN) and i != len(enabled_moves) - 1:
                                enabled_moves[i], enabled_moves[i+1] = enabled_moves[i+1], enabled_moves[i]
                            imgui.same_line()
                            if imgui.checkbox(item,True)[0]:
                                disabled_moves.append(enabled_moves.pop(i))
                            if len(disabled_moves) not in [0,4]:
                                imgui.separator()
                        for i, item in enumerate(disabled_moves):
                            if imgui.checkbox(item,False)[0]:
                                enabled_moves.append(disabled_moves.pop(i))
                        if ",".join(enabled_moves) == 'push,enter,eat,possess':
                            rb.usefulVal.pop("LAO",None)
                        else: rb.usefulVal["LAO"] = ",".join(enabled_moves)
                        imgui.end_menu()    
                    imgui.end_menu()
     