
import {ReflexEvent,applyEventActions,isTrue} from "$/utils/state"
import {StateContexts,addEvents} from "$/utils/context"
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {jsx} from "@emotion/react"
import {Box as RadixThemesBox,Button as RadixThemesButton,Flex as RadixThemesFlex,Link as RadixThemesLink,Text as RadixThemesText} from "@radix-ui/themes"
import {Link as ReactRouterLink} from "react-router"
import LucideUsers from "lucide-react/dist/esm/icons/users.mjs"
import LucideTarget from "lucide-react/dist/esm/icons/target.mjs"
import LucideSettings from "lucide-react/dist/esm/icons/settings.mjs"
import LucideRefreshCw from "lucide-react/dist/esm/icons/refresh-cw.mjs"
import LucideLogOut from "lucide-react/dist/esm/icons/log-out.mjs"
import LucideFileText from "lucide-react/dist/esm/icons/file-text.mjs"
import LucideLayoutDashboard from "lucide-react/dist/esm/icons/layout-dashboard.mjs"
import LucideUpload from "lucide-react/dist/esm/icons/upload.mjs"








export const Cond_comp_67121af271f156e6a0cc565de2340466_fb5998e9 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state)



    return(
        (reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state.expanded_rx_state_?(children?.at?.(0)):(children?.at?.(1)))
    )
});

export const Button_button_519144b0c11761ab606306dddccf4def_fb5998e9 = memo(({children}) => {
    const on_click_57ce2ca0f16f026b333dd53eb1912df6 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.back_end___interface___state___sidebar_state____sidebar_state.toggle_sidebar", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx(RadixThemesButton,{css:({ ["background"] : "transparent", ["color"] : "rgba(255, 255, 255, 0.68)", ["padding"] : "0.5rem", ["minWidth"] : "auto", ["height"] : "auto", ["cursor"] : "pointer", ["borderRadius"] : "8px", ["&:hover"] : ({ ["background"] : "#124E8A", ["color"] : "#FFFFFF" }) }),onClick:on_click_57ce2ca0f16f026b333dd53eb1912df6},children)
    )
});

export const Link_link_95b6245e75600e5e02956148a622eaa5_fb5998e9 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state)



    return(
        jsx(RadixThemesLink,{asChild:true,css:({ ["width"] : "100%", ["padding"] : "0.75rem 1rem", ["borderRadius"] : "8px", ["textDecoration"] : "none", ["transition"] : "all 0.2s ease", ["&:hover"] : ({ ["background"] : "#124E8A" }) })},jsx(ReactRouterLink,{to:"/admin"},jsx(RadixThemesFlex,{align:"center",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"row",gap:"3"},jsx(LucideLayoutDashboard,{css:({ ["color"] : "rgba(255, 255, 255, 0.68)" }),size:20},),jsx(Fragment,{},(reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state.expanded_rx_state_?(jsx(Fragment,{},jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "0.875rem", ["fontWeight"] : "500", ["color"] : "#FFFFFF", ["whiteSpace"] : "nowrap" })},"Vis\u00e3o Geral"))):(jsx(Fragment,{},)))))))
    )
});

export const Link_link_7045abebfb0972eafe878ee767724ec2_fb5998e9 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state)



    return(
        jsx(RadixThemesLink,{asChild:true,css:({ ["width"] : "100%", ["padding"] : "0.75rem 1rem", ["borderRadius"] : "8px", ["textDecoration"] : "none", ["transition"] : "all 0.2s ease", ["&:hover"] : ({ ["background"] : "#124E8A" }) })},jsx(ReactRouterLink,{to:"/admin/metas"},jsx(RadixThemesFlex,{align:"center",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"row",gap:"3"},jsx(LucideTarget,{css:({ ["color"] : "rgba(255, 255, 255, 0.68)" }),size:20},),jsx(Fragment,{},(reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state.expanded_rx_state_?(jsx(Fragment,{},jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "0.875rem", ["fontWeight"] : "500", ["color"] : "#FFFFFF", ["whiteSpace"] : "nowrap" })},"Metas"))):(jsx(Fragment,{},)))))))
    )
});

export const Link_link_afc5698f5584dbc141a918af4bb7aa2d_fb5998e9 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state)



    return(
        jsx(RadixThemesLink,{asChild:true,css:({ ["width"] : "100%", ["padding"] : "0.75rem 1rem", ["borderRadius"] : "8px", ["textDecoration"] : "none", ["transition"] : "all 0.2s ease", ["&:hover"] : ({ ["background"] : "#124E8A" }) })},jsx(ReactRouterLink,{to:"/admin/integracoes"},jsx(RadixThemesFlex,{align:"center",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"row",gap:"3"},jsx(LucideRefreshCw,{css:({ ["color"] : "rgba(255, 255, 255, 0.68)" }),size:20},),jsx(Fragment,{},(reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state.expanded_rx_state_?(jsx(Fragment,{},jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "0.875rem", ["fontWeight"] : "500", ["color"] : "#FFFFFF", ["whiteSpace"] : "nowrap" })},"Integra\u00e7\u00f5es"))):(jsx(Fragment,{},)))))))
    )
});

export const Link_link_0e5d0685a7f8194b14fa131bb2555983_fb5998e9 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state)



    return(
        jsx(RadixThemesLink,{asChild:true,css:({ ["width"] : "100%", ["padding"] : "0.75rem 1rem", ["borderRadius"] : "8px", ["textDecoration"] : "none", ["transition"] : "all 0.2s ease", ["&:hover"] : ({ ["background"] : "#124E8A" }) })},jsx(ReactRouterLink,{to:"/admin/importacoes"},jsx(RadixThemesFlex,{align:"center",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"row",gap:"3"},jsx(LucideUpload,{css:({ ["color"] : "rgba(255, 255, 255, 0.68)" }),size:20},),jsx(Fragment,{},(reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state.expanded_rx_state_?(jsx(Fragment,{},jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "0.875rem", ["fontWeight"] : "500", ["color"] : "#FFFFFF", ["whiteSpace"] : "nowrap" })},"Importa\u00e7\u00f5es"))):(jsx(Fragment,{},)))))))
    )
});

export const Link_link_62cbedb34f093ffbba555f0bea6f63b9_fb5998e9 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state)



    return(
        jsx(RadixThemesLink,{asChild:true,css:({ ["width"] : "100%", ["padding"] : "0.75rem 1rem", ["borderRadius"] : "8px", ["textDecoration"] : "none", ["transition"] : "all 0.2s ease", ["&:hover"] : ({ ["background"] : "#124E8A" }) })},jsx(ReactRouterLink,{to:"/admin/relatorios"},jsx(RadixThemesFlex,{align:"center",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"row",gap:"3"},jsx(LucideFileText,{css:({ ["color"] : "rgba(255, 255, 255, 0.68)" }),size:20},),jsx(Fragment,{},(reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state.expanded_rx_state_?(jsx(Fragment,{},jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "0.875rem", ["fontWeight"] : "500", ["color"] : "#FFFFFF", ["whiteSpace"] : "nowrap" })},"Relat\u00f3rios"))):(jsx(Fragment,{},)))))))
    )
});

export const Link_link_9ef4db4dc7345163b69eb96911c46905_fb5998e9 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state)



    return(
        jsx(RadixThemesLink,{asChild:true,css:({ ["width"] : "100%", ["padding"] : "0.75rem 1rem", ["borderRadius"] : "8px", ["textDecoration"] : "none", ["transition"] : "all 0.2s ease", ["&:hover"] : ({ ["background"] : "#124E8A" }) })},jsx(ReactRouterLink,{to:"/admin/usuarios"},jsx(RadixThemesFlex,{align:"center",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"row",gap:"3"},jsx(LucideUsers,{css:({ ["color"] : "rgba(255, 255, 255, 0.68)" }),size:20},),jsx(Fragment,{},(reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state.expanded_rx_state_?(jsx(Fragment,{},jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "0.875rem", ["fontWeight"] : "500", ["color"] : "#FFFFFF", ["whiteSpace"] : "nowrap" })},"Usu\u00e1rios"))):(jsx(Fragment,{},)))))))
    )
});

export const Link_link_48bb0153c325683807f6adb91a28b8e8_fb5998e9 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state)



    return(
        jsx(RadixThemesLink,{asChild:true,css:({ ["width"] : "100%", ["padding"] : "0.75rem 1rem", ["borderRadius"] : "8px", ["textDecoration"] : "none", ["transition"] : "all 0.2s ease", ["&:hover"] : ({ ["background"] : "#124E8A" }) })},jsx(ReactRouterLink,{to:"/admin/configuracoes"},jsx(RadixThemesFlex,{align:"center",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"row",gap:"3"},jsx(LucideSettings,{css:({ ["color"] : "rgba(255, 255, 255, 0.68)" }),size:20},),jsx(Fragment,{},(reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state.expanded_rx_state_?(jsx(Fragment,{},jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "0.875rem", ["fontWeight"] : "500", ["color"] : "#FFFFFF", ["whiteSpace"] : "nowrap" })},"Configura\u00e7\u00f5es"))):(jsx(Fragment,{},)))))))
    )
});

export const Link_link_c403380f16ffb3cf2873618f4b8c0c3e_fb5998e9 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state)



    return(
        jsx(RadixThemesLink,{asChild:true,css:({ ["width"] : "100%", ["padding"] : "0.75rem 1rem", ["borderRadius"] : "8px", ["textDecoration"] : "none", ["transition"] : "all 0.2s ease", ["&:hover"] : ({ ["background"] : "#124E8A" }) })},jsx(ReactRouterLink,{to:"/logout"},jsx(RadixThemesFlex,{align:"center",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"row",gap:"3"},jsx(LucideLogOut,{css:({ ["color"] : "rgba(255, 255, 255, 0.68)" }),size:20},),jsx(Fragment,{},(reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state.expanded_rx_state_?(jsx(Fragment,{},jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "0.875rem", ["fontWeight"] : "500", ["color"] : "#FFFFFF", ["whiteSpace"] : "nowrap" })},"Sair"))):(jsx(Fragment,{},)))))))
    )
});

export const Box_box_e985d96aaba2aeb9626b45455454be27_fb5998e9 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state)



    return(
        jsx(RadixThemesBox,{css:({ ["background"] : "#272361", ["width"] : (reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state.expanded_rx_state_ ? "260px" : "76px"), ["minWidth"] : (reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state.expanded_rx_state_ ? "260px" : "76px"), ["height"] : "100vh", ["padding"] : "1rem", ["transition"] : "width 0.25s ease, min-width 0.25s ease", ["fontFamily"] : "Roboto, Helvetica, sans-serif", ["--default-font-family"] : "Roboto, Helvetica, sans-serif", ["overflow"] : "hidden" })},children)
    )
});

export const Bare_comp_e777933c0c74bcb2acf22e232bf3c62f_fb5998e9 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state)



    return(
        reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state.error_message_rx_state_
    )
});

export const Bare_comp_766ecb98ca0ca96a20f8d8d36f47b232_fb5998e9 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state)



    return(
        reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state.codigo_atual_rx_state_
    )
});

export const Bare_comp_c49a9a1380496c94e0491dfc4036644b_fb5998e9 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state)



    return(
        reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state.titulo_rx_state_
    )
});

export const Bare_comp_8e914451979e664345f3dbb971161851_fb5998e9 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state)



    return(
        reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state.eixo_rx_state_
    )
});

export const Bare_comp_0367889d7f8647ff3949358a2a3e1991_fb5998e9 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state)



    return(
        reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state.andamento_rx_state_
    )
});

export const Bare_comp_9a75e5efc2d7d9749eee71fcc73fcf39_fb5998e9 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state)



    return(
        reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state.situacao_rx_state_
    )
});

export const Bare_comp_3739c1543a8c966e00110fa458d9c636_fb5998e9 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state)



    return(
        reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state.prazo_rx_state_
    )
});

export const Foreach_comp_9b707d8af113b912ff53b1ad405feacf_fb5998e9 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state)



    return(
        Array.prototype.map.call(reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state.orgaos_rx_state_ ?? [],((value_rx_state_,index_3cc36a291ced33d1f2c3b034c64f0d47)=>(jsx(RadixThemesText,{as:"p",css:({ ["color"] : "#272361", ["fontSize"] : "0.9rem" }),key:index_3cc36a291ced33d1f2c3b034c64f0d47},value_rx_state_))))
    )
});

export const Foreach_comp_0314eff07eb08b9aed9fc9b5588ad3d0_fb5998e9 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state)



    return(
        Array.prototype.map.call(reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state.ods_rx_state_ ?? [],((value_rx_state_,index_3cc36a291ced33d1f2c3b034c64f0d47)=>(jsx(RadixThemesText,{as:"p",css:({ ["color"] : "#272361", ["fontSize"] : "0.9rem" }),key:index_3cc36a291ced33d1f2c3b034c64f0d47},value_rx_state_))))
    )
});

export const Bare_comp_846f7cb7ee4778ffbe524c874e620a84_fb5998e9 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state)



    return(
        reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state.contexto_rx_state_
    )
});

export const Bare_comp_1a2ffef97022eed89409b680d5b137f8_fb5998e9 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state)



    return(
        reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state.previsao_rx_state_
    )
});

export const Bare_comp_ab48049228864a241bbd2bade7f0c569_fb5998e9 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state)



    return(
        reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state.empenhado_rx_state_
    )
});

export const Bare_comp_cdd59aae659724f6c96e9bd69cca5342_fb5998e9 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state)



    return(
        reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state.liquidado_rx_state_
    )
});

export const Foreach_comp_07e46d2b0fe234ea4c54da204230def1_fb5998e9 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state)



    return(
        Array.prototype.map.call(reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state.iniciativas_rx_state_ ?? [],((value_rx_state_,index_3cc36a291ced33d1f2c3b034c64f0d47)=>(jsx(RadixThemesText,{as:"p",css:({ ["color"] : "#272361", ["fontSize"] : "0.9rem" }),key:index_3cc36a291ced33d1f2c3b034c64f0d47},value_rx_state_))))
    )
});

export const Cond_comp_08da89dbc84a5060f470a3c67a461130_fb5998e9 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state)



    return(
        ((reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state.iniciativas_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});

export const Cond_comp_919d9d6406f1ccc7a076956b5cc4b215_fb5998e9 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state)



    return(
        (reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state.ficha_encontrada_rx_state_?(children?.at?.(0)):(children?.at?.(1)))
    )
});

export const Cond_comp_18e9cfeb608e93dab7fa60ab71731f97_fb5998e9 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state)



    return(
        (!((reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state.error_message_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});

export const Cond_comp_51d821a69871215c7672ac5379a3766e_fb5998e9 = memo(({children}) => {
    const reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state = useContext(StateContexts.reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state)



    return(
        (reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state.loading_rx_state_?(children?.at?.(0)):(children?.at?.(1)))
    )
});
