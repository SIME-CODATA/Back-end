import {Flex as RadixThemesFlex,Spinner as RadixThemesSpinner,Text as RadixThemesText} from "@radix-ui/themes"
import {Fragment,useEffect} from "react"
import {jsx} from "@emotion/react"





export default function Component() {





  return (
    jsx(Fragment,{},jsx(RadixThemesFlex,{css:({ ["display"] : "flex", ["alignItems"] : "center", ["justifyContent"] : "center", ["minHeight"] : "100vh" })},jsx(RadixThemesFlex,{align:"center",className:"rx-Stack",direction:"column",gap:"4"},jsx(RadixThemesSpinner,{size:"3"},),jsx(RadixThemesText,{as:"p",color:"gray"},"Encerrando sess\u00e3o..."))),jsx("title",{},"Saindo | Programa de Metas"),jsx("meta",{content:"favicon.ico",property:"og:image"},))
  )
}