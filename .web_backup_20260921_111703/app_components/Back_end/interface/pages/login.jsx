
import {ReflexEvent,applyEventActions,getRefValue,getRefValues,isTrue} from "$/utils/state"
import {StateContexts,addEvents} from "$/utils/context"
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {jsx} from "@emotion/react"
import {Root as RadixFormRoot} from "@radix-ui/react-form"








export const Bare_comp_7c3bcf24aa613504cbb144c99c346f39_bacf5e40 = memo(({children}) => {
    const reflex___state____state__back_end___access___states___auth_state____auth_state = useContext(StateContexts.reflex___state____state__back_end___access___states___auth_state____auth_state)



    return(
        reflex___state____state__back_end___access___states___auth_state____auth_state.error_message_rx_state_
    )
});

export const Cond_comp_7cf0f201be9416972f192f517a0d5081_bacf5e40 = memo(({children}) => {
    const reflex___state____state__back_end___access___states___auth_state____auth_state = useContext(StateContexts.reflex___state____state__back_end___access___states___auth_state____auth_state)



    return(
        (!((reflex___state____state__back_end___access___states___auth_state____auth_state.error_message_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});

export const Form_root_956a474346f2196948e4623ad6b2d2a3_bacf5e40 = memo(({children}) => {
    

    const handleSubmit_479164421292f2fc1363bf2178705a32 = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({  })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.back_end___access___states___auth_state____auth_state.login", ({ ["form_data"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    


    return(
        jsx(RadixFormRoot,{className:"Root ",css:({ ["width"] : "100%" }),onSubmit:handleSubmit_479164421292f2fc1363bf2178705a32},children)
    )
});
