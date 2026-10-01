
import {ReflexEvent,applyEventActions,isTrue} from "$/utils/state"
import {StateContexts,addEvents} from "$/utils/context"
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {jsx} from "@emotion/react"
import {Box as RadixThemesBox,Button as RadixThemesButton,Flex as RadixThemesFlex,Link as RadixThemesLink,Progress as RadixThemesProgress,Text as RadixThemesText} from "@radix-ui/themes"
import {Link as ReactRouterLink} from "react-router"
import LucideUsers from "lucide-react/dist/esm/icons/users.mjs"
import LucideTarget from "lucide-react/dist/esm/icons/target.mjs"
import LucideSettings from "lucide-react/dist/esm/icons/settings.mjs"
import LucideRefreshCw from "lucide-react/dist/esm/icons/refresh-cw.mjs"
import LucideLogOut from "lucide-react/dist/esm/icons/log-out.mjs"
import LucideFileText from "lucide-react/dist/esm/icons/file-text.mjs"
import LucideLayoutDashboard from "lucide-react/dist/esm/icons/layout-dashboard.mjs"
import LucideUpload from "lucide-react/dist/esm/icons/upload.mjs"








export const Cond_comp_67121af271f156e6a0cc565de2340466_e2ee63f4 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state)



    return(
        (reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state.expanded_rx_state_?(children?.at?.(0)):(children?.at?.(1)))
    )
});

export const Button_button_519144b0c11761ab606306dddccf4def_e2ee63f4 = memo(({children}) => {
    const on_click_57ce2ca0f16f026b333dd53eb1912df6 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.back_end___interface___state___sidebar_state____sidebar_state.toggle_sidebar", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx(RadixThemesButton,{css:({ ["background"] : "transparent", ["color"] : "rgba(255, 255, 255, 0.68)", ["padding"] : "0.5rem", ["minWidth"] : "auto", ["height"] : "auto", ["cursor"] : "pointer", ["borderRadius"] : "8px", ["&:hover"] : ({ ["background"] : "#124E8A", ["color"] : "#FFFFFF" }) }),onClick:on_click_57ce2ca0f16f026b333dd53eb1912df6},children)
    )
});

export const Link_link_95b6245e75600e5e02956148a622eaa5_e2ee63f4 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state)



    return(
        jsx(RadixThemesLink,{asChild:true,css:({ ["width"] : "100%", ["padding"] : "0.75rem 1rem", ["borderRadius"] : "8px", ["textDecoration"] : "none", ["transition"] : "all 0.2s ease", ["&:hover"] : ({ ["background"] : "#124E8A" }) })},jsx(ReactRouterLink,{to:"/admin"},jsx(RadixThemesFlex,{align:"center",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"row",gap:"3"},jsx(LucideLayoutDashboard,{css:({ ["color"] : "rgba(255, 255, 255, 0.68)" }),size:20},),jsx(Fragment,{},(reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state.expanded_rx_state_?(jsx(Fragment,{},jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "0.875rem", ["fontWeight"] : "500", ["color"] : "#FFFFFF", ["whiteSpace"] : "nowrap" })},"Vis\u00e3o Geral"))):(jsx(Fragment,{},)))))))
    )
});

export const Link_link_7045abebfb0972eafe878ee767724ec2_e2ee63f4 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state)



    return(
        jsx(RadixThemesLink,{asChild:true,css:({ ["width"] : "100%", ["padding"] : "0.75rem 1rem", ["borderRadius"] : "8px", ["textDecoration"] : "none", ["transition"] : "all 0.2s ease", ["&:hover"] : ({ ["background"] : "#124E8A" }) })},jsx(ReactRouterLink,{to:"/admin/metas"},jsx(RadixThemesFlex,{align:"center",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"row",gap:"3"},jsx(LucideTarget,{css:({ ["color"] : "rgba(255, 255, 255, 0.68)" }),size:20},),jsx(Fragment,{},(reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state.expanded_rx_state_?(jsx(Fragment,{},jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "0.875rem", ["fontWeight"] : "500", ["color"] : "#FFFFFF", ["whiteSpace"] : "nowrap" })},"Metas"))):(jsx(Fragment,{},)))))))
    )
});

export const Link_link_afc5698f5584dbc141a918af4bb7aa2d_e2ee63f4 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state)



    return(
        jsx(RadixThemesLink,{asChild:true,css:({ ["width"] : "100%", ["padding"] : "0.75rem 1rem", ["borderRadius"] : "8px", ["textDecoration"] : "none", ["transition"] : "all 0.2s ease", ["&:hover"] : ({ ["background"] : "#124E8A" }) })},jsx(ReactRouterLink,{to:"/admin/integracoes"},jsx(RadixThemesFlex,{align:"center",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"row",gap:"3"},jsx(LucideRefreshCw,{css:({ ["color"] : "rgba(255, 255, 255, 0.68)" }),size:20},),jsx(Fragment,{},(reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state.expanded_rx_state_?(jsx(Fragment,{},jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "0.875rem", ["fontWeight"] : "500", ["color"] : "#FFFFFF", ["whiteSpace"] : "nowrap" })},"Integra\u00e7\u00f5es"))):(jsx(Fragment,{},)))))))
    )
});

export const Link_link_0e5d0685a7f8194b14fa131bb2555983_e2ee63f4 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state)



    return(
        jsx(RadixThemesLink,{asChild:true,css:({ ["width"] : "100%", ["padding"] : "0.75rem 1rem", ["borderRadius"] : "8px", ["textDecoration"] : "none", ["transition"] : "all 0.2s ease", ["&:hover"] : ({ ["background"] : "#124E8A" }) })},jsx(ReactRouterLink,{to:"/admin/importacoes"},jsx(RadixThemesFlex,{align:"center",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"row",gap:"3"},jsx(LucideUpload,{css:({ ["color"] : "rgba(255, 255, 255, 0.68)" }),size:20},),jsx(Fragment,{},(reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state.expanded_rx_state_?(jsx(Fragment,{},jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "0.875rem", ["fontWeight"] : "500", ["color"] : "#FFFFFF", ["whiteSpace"] : "nowrap" })},"Importa\u00e7\u00f5es"))):(jsx(Fragment,{},)))))))
    )
});

export const Link_link_62cbedb34f093ffbba555f0bea6f63b9_e2ee63f4 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state)



    return(
        jsx(RadixThemesLink,{asChild:true,css:({ ["width"] : "100%", ["padding"] : "0.75rem 1rem", ["borderRadius"] : "8px", ["textDecoration"] : "none", ["transition"] : "all 0.2s ease", ["&:hover"] : ({ ["background"] : "#124E8A" }) })},jsx(ReactRouterLink,{to:"/admin/relatorios"},jsx(RadixThemesFlex,{align:"center",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"row",gap:"3"},jsx(LucideFileText,{css:({ ["color"] : "rgba(255, 255, 255, 0.68)" }),size:20},),jsx(Fragment,{},(reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state.expanded_rx_state_?(jsx(Fragment,{},jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "0.875rem", ["fontWeight"] : "500", ["color"] : "#FFFFFF", ["whiteSpace"] : "nowrap" })},"Relat\u00f3rios"))):(jsx(Fragment,{},)))))))
    )
});

export const Link_link_9ef4db4dc7345163b69eb96911c46905_e2ee63f4 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state)



    return(
        jsx(RadixThemesLink,{asChild:true,css:({ ["width"] : "100%", ["padding"] : "0.75rem 1rem", ["borderRadius"] : "8px", ["textDecoration"] : "none", ["transition"] : "all 0.2s ease", ["&:hover"] : ({ ["background"] : "#124E8A" }) })},jsx(ReactRouterLink,{to:"/admin/usuarios"},jsx(RadixThemesFlex,{align:"center",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"row",gap:"3"},jsx(LucideUsers,{css:({ ["color"] : "rgba(255, 255, 255, 0.68)" }),size:20},),jsx(Fragment,{},(reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state.expanded_rx_state_?(jsx(Fragment,{},jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "0.875rem", ["fontWeight"] : "500", ["color"] : "#FFFFFF", ["whiteSpace"] : "nowrap" })},"Usu\u00e1rios"))):(jsx(Fragment,{},)))))))
    )
});

export const Link_link_48bb0153c325683807f6adb91a28b8e8_e2ee63f4 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state)



    return(
        jsx(RadixThemesLink,{asChild:true,css:({ ["width"] : "100%", ["padding"] : "0.75rem 1rem", ["borderRadius"] : "8px", ["textDecoration"] : "none", ["transition"] : "all 0.2s ease", ["&:hover"] : ({ ["background"] : "#124E8A" }) })},jsx(ReactRouterLink,{to:"/admin/configuracoes"},jsx(RadixThemesFlex,{align:"center",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"row",gap:"3"},jsx(LucideSettings,{css:({ ["color"] : "rgba(255, 255, 255, 0.68)" }),size:20},),jsx(Fragment,{},(reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state.expanded_rx_state_?(jsx(Fragment,{},jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "0.875rem", ["fontWeight"] : "500", ["color"] : "#FFFFFF", ["whiteSpace"] : "nowrap" })},"Configura\u00e7\u00f5es"))):(jsx(Fragment,{},)))))))
    )
});

export const Link_link_c403380f16ffb3cf2873618f4b8c0c3e_e2ee63f4 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state)



    return(
        jsx(RadixThemesLink,{asChild:true,css:({ ["width"] : "100%", ["padding"] : "0.75rem 1rem", ["borderRadius"] : "8px", ["textDecoration"] : "none", ["transition"] : "all 0.2s ease", ["&:hover"] : ({ ["background"] : "#124E8A" }) })},jsx(ReactRouterLink,{to:"/logout"},jsx(RadixThemesFlex,{align:"center",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"row",gap:"3"},jsx(LucideLogOut,{css:({ ["color"] : "rgba(255, 255, 255, 0.68)" }),size:20},),jsx(Fragment,{},(reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state.expanded_rx_state_?(jsx(Fragment,{},jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "0.875rem", ["fontWeight"] : "500", ["color"] : "#FFFFFF", ["whiteSpace"] : "nowrap" })},"Sair"))):(jsx(Fragment,{},)))))))
    )
});

export const Box_box_e985d96aaba2aeb9626b45455454be27_e2ee63f4 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state)



    return(
        jsx(RadixThemesBox,{css:({ ["background"] : "#272361", ["width"] : (reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state.expanded_rx_state_ ? "260px" : "76px"), ["minWidth"] : (reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state.expanded_rx_state_ ? "260px" : "76px"), ["height"] : "100vh", ["padding"] : "1rem", ["transition"] : "width 0.25s ease, min-width 0.25s ease", ["fontFamily"] : "Roboto, Helvetica, sans-serif", ["--default-font-family"] : "Roboto, Helvetica, sans-serif", ["overflow"] : "hidden" })},children)
    )
});

export const Bare_comp_17a9af5e88ae1df58b6adff3515c6492_e2ee63f4 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state)



    return(
        reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state.ultima_sincronizacao_rx_state_
    )
});

export const Bare_comp_f3432772c648bf73dfc4360ce9506d16_e2ee63f4 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state)



    return(
        (reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state.loading_rx_state_ ? "Atualizando..." : "Atualizar dados")
    )
});

export const Button_button_5d344eb8b559b5eeae58f7c9ad6c9121_e2ee63f4 = memo(({children}) => {
    const on_click_3d16ab4931ed61fa9e9e631911301508 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.back_end___interface___state___dashboard_state____dashboard_state.refresh_data", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state)



    return(
        jsx(RadixThemesButton,{css:({ ["background"] : "#2C286D", ["color"] : "white", ["borderRadius"] : "7px", ["paddingInlineStart"] : "1rem", ["paddingInlineEnd"] : "1rem", ["cursor"] : "pointer", ["&:hover"] : ({ ["background"] : "#124E8A" }) }),disabled:reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state.loading_rx_state_,onClick:on_click_3d16ab4931ed61fa9e9e631911301508},children)
    )
});

export const Bare_comp_f93ff946e5a99cd1da7f1271c9704346_e2ee63f4 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state)



    return(
        reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state.sync_message_rx_state_
    )
});

export const Cond_comp_9ebd1e30960a3399499ce15a4aed5ecb_e2ee63f4 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state)



    return(
        (!((reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state.sync_message_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});

export const Bare_comp_0cd738ad231c48ebd33accea5531c17c_e2ee63f4 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state)



    return(
        reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state.error_message_rx_state_
    )
});

export const Cond_comp_7f72bfc1e698733979a6a5e680233022_e2ee63f4 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state)



    return(
        (!((reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state.error_message_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});

export const Foreach_comp_adfb9f7df30f005e5ba19b54d92c82ed_e2ee63f4 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state)



    return(
        Array.prototype.map.call(reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state.eixos_resumo_rx_state_ ?? [],((axis_rx_state_,index_64d5287b5aea99155a46218559dcfa25)=>(jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"column",key:index_64d5287b5aea99155a46218559dcfa25,gap:"2"},jsx(RadixThemesBox,{css:({ ["background"] : ((axis_rx_state_?.["nome"]?.valueOf?.() === "Universo SP"?.valueOf?.()) ? "#3ABB4B" : ((axis_rx_state_?.["nome"]?.valueOf?.() === "Viver S\u00e3o Paulo"?.valueOf?.()) ? "#FF641E" : ((axis_rx_state_?.["nome"]?.valueOf?.() === "Cidade Empreendedora"?.valueOf?.()) ? "#1400C8" : "#87314F"))), ["width"] : "100%", ["minHeight"] : "104px", ["display"] : "flex", ["alignItems"] : "center", ["justifyContent"] : "center", ["position"] : "relative", ["botton"] : "2rem", ["borderTopRightRadius"] : "60px" })},jsx(RadixThemesFlex,{align:"center",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"column",justify:"center",gap:"2"},jsx(RadixThemesFlex,{align:"end",className:"rx-Stack",direction:"row",gap:"1"},jsx(RadixThemesText,{as:"p",css:({ ["color"] : "white", ["fontSize"] : "2rem", ["fontWeight"] : "700", ["lineHeight"] : "1" })},axis_rx_state_?.["quantidade"]),jsx(RadixThemesText,{as:"p",css:({ ["color"] : "white", ["fontSize"] : "0.7rem", ["fontWeight"] : "700" })},"METAS")),jsx(RadixThemesText,{as:"p",css:({ ["color"] : "white", ["fontSize"] : "0.78rem", ["fontWeight"] : "700", ["textTransform"] : "uppercase" })},axis_rx_state_?.["nome"]))),jsx(RadixThemesBox,{css:({ ["background"] : ((axis_rx_state_?.["nome"]?.valueOf?.() === "Universo SP"?.valueOf?.()) ? "#3ABB4B" : ((axis_rx_state_?.["nome"]?.valueOf?.() === "Viver S\u00e3o Paulo"?.valueOf?.()) ? "#FF641E" : ((axis_rx_state_?.["nome"]?.valueOf?.() === "Cidade Empreendedora"?.valueOf?.()) ? "#1400C8" : "#87314F"))), ["width"] : "100%", ["padding"] : "0.9rem" })},jsx(RadixThemesFlex,{align:"center",className:"rx-Stack",direction:"row",justify:"center",gap:"2"},jsx(RadixThemesText,{as:"p",css:({ ["color"] : "white", ["fontSize"] : "1.25rem", ["fontWeight"] : "700" })},axis_rx_state_?.["atingidas"]),jsx(RadixThemesText,{as:"p",css:({ ["color"] : "white", ["fontSize"] : "0.72rem", ["fontWeight"] : "700" })},"ATINGIDAS")))))))
    )
});

export const Bare_comp_dc14f99b34a268fc636815137aa8b659_e2ee63f4 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state)



    return(
        reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state.total_metas_rx_state_
    )
});

export const Bare_comp_116ce04f505b6878144a46346e9aa981_e2ee63f4 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state)



    return(
        reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state.metas_atingidas_rx_state_
    )
});

export const Bare_comp_a0dee50e7ead43a4ee535ae8bfcc3877_e2ee63f4 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state)



    return(
        reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state.percentual_atingidas_rx_state_
    )
});

export const Progress_progress_505568043986184060fa964a98926c3f_e2ee63f4 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state)



    return(
        jsx(RadixThemesProgress,{color:"green",css:({ ["width"] : "100%" }),max:reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state.total_metas_rx_state_,value:reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state.metas_atingidas_rx_state_},)
    )
});

export const Bare_comp_a74c343bbf09ed64d0436696ffb09abe_e2ee63f4 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state)



    return(
        reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state.metas_em_progresso_rx_state_
    )
});

export const Bare_comp_f9571d581150cad1dc37f19cff075a2a_e2ee63f4 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state)



    return(
        reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state.percentual_em_progresso_rx_state_
    )
});

export const Progress_progress_89f8efb4df50108ee5add6c4ddeb0fed_e2ee63f4 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state)



    return(
        jsx(RadixThemesProgress,{color:"cyan",css:({ ["width"] : "100%" }),max:reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state.total_metas_rx_state_,value:reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state.metas_em_progresso_rx_state_},)
    )
});

export const Bare_comp_ba32ebcc0b15257cabaad3a92086c25e_e2ee63f4 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state)



    return(
        reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state.metas_em_planejamento_rx_state_
    )
});

export const Bare_comp_5afcc222b123fa129b6c3211f5ffcda4_e2ee63f4 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state)



    return(
        reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state.percentual_em_planejamento_rx_state_
    )
});

export const Progress_progress_9bc2cffbba042bc363837cc428d79244_e2ee63f4 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state)



    return(
        jsx(RadixThemesProgress,{color:"orange",css:({ ["width"] : "100%" }),max:reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state.total_metas_rx_state_,value:reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state.metas_em_planejamento_rx_state_},)
    )
});

export const Foreach_comp_63961e9a2632b11786d1cb95087aff45_e2ee63f4 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state)



    return(
        Array.prototype.map.call(reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state.situacao_resumo_rx_state_ ?? [],((item_rx_state_,index_0a6338c79d93c8a1c66fafbbfd746d4a)=>(jsx(RadixThemesFlex,{align:"center",className:"rx-Stack",css:({ ["width"] : "100%", ["paddingTop"] : "0.25rem", ["paddingBottom"] : "0.25rem" }),direction:"row",key:index_0a6338c79d93c8a1c66fafbbfd746d4a,gap:"3"},jsx(RadixThemesText,{as:"p",css:({ ["color"] : "#272361", ["fontSize"] : "0.875rem" })},item_rx_state_?.["nome"]),jsx(RadixThemesFlex,{css:({ ["flex"] : 1, ["justifySelf"] : "stretch", ["alignSelf"] : "stretch" })},),jsx(RadixThemesBox,{css:({ ["background"] : "#1287B2", ["borderRadius"] : "4px", ["minWidth"] : "38px", ["padding"] : "0.3rem 0.55rem", ["textAlign"] : "center" })},jsx(RadixThemesText,{as:"p",css:({ ["color"] : "white", ["fontSize"] : "0.875rem", ["fontWeight"] : "700" })},item_rx_state_?.["quantidade"]))))))
    )
});

export const Foreach_comp_54fef46f9af576649d1501f6e56fc632_e2ee63f4 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state)



    return(
        Array.prototype.map.call(reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state.prazo_resumo_rx_state_ ?? [],((item_rx_state_,index_2b90e8bffb677abaaa54bcf52a99bd6c)=>(jsx(RadixThemesFlex,{align:"center",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"row",key:index_2b90e8bffb677abaaa54bcf52a99bd6c,gap:"3"},jsx(RadixThemesBox,{css:({ ["background"] : "#1287B2", ["borderRadius"] : "3px", ["width"] : "42px", ["minWidth"] : "42px", ["paddingTop"] : "0.4rem", ["paddingBottom"] : "0.4rem", ["textAlign"] : "center" })},jsx(RadixThemesText,{as:"p",css:({ ["color"] : "white", ["fontWeight"] : "700", ["fontSize"] : "0.875rem" })},item_rx_state_?.["quantidade"])),jsx(RadixThemesText,{as:"p",css:({ ["color"] : "#272361", ["fontSize"] : "0.875rem" })},item_rx_state_?.["nome"])))))
    )
});

export const Bare_comp_b86c62c5ca040d77061c5edb272b0db0_e2ee63f4 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state)



    return(
        reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state.orcamento_previsao_rx_state_
    )
});

export const Bare_comp_dbbbf2efa32bc57b34d74df4bb93c296_e2ee63f4 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state)



    return(
        reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state.orcamento_empenhado_rx_state_
    )
});

export const Bare_comp_37c330ed0da858357d3f55eb8fe60005_e2ee63f4 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state)



    return(
        reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state.percentual_empenhado_rx_state_
    )
});

export const Bare_comp_7a7eb3bbb6d6d53bd24f1fc376b6249d_e2ee63f4 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state)



    return(
        reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state.orcamento_liquidado_rx_state_
    )
});

export const Bare_comp_5e4148f0566781ed588bc69502913fd0_e2ee63f4 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state)



    return(
        reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state.percentual_liquidado_rx_state_
    )
});

export const Bare_comp_3f35897e71ffa3282265f20d0e37334b_e2ee63f4 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state)



    return(
        reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state.metas_com_previsao_rx_state_
    )
});

export const Vstack_flex_45d695c4eca50c75d6e5602e521b60b5_e2ee63f4 = memo(({children}) => {
    
                useEffect(() => {
                    ((...args) => (addEvents([(ReflexEvent("reflex___state____state.back_end___interface___state___dashboard_state____dashboard_state.load_summary", ({  }), ({  })))], args, ({  }))))()
                    return () => {
                        
                    }
                }, []);



    return(
        jsx(RadixThemesFlex,{align:"stretch",className:"rx-Stack",css:({ ["width"] : "100%", ["paddingBottom"] : "2rem" }),direction:"column",gap:"7"},children)
    )
});
