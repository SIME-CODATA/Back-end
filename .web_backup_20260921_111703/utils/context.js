import { createContext, useContext, useMemo, useReducer, useState, createElement, useEffect } from "react"
import { applyDelta, ReflexEvent, hydrateClientStorage, useEventLoop, refs } from "$/utils/state"
import { jsx } from "@emotion/react";

export const initialState = {"reflex___state____state": {"codigo_rx_state_": "", "is_hydrated_rx_state_": false, "router_rx_state_": {"session": {"client_token": "", "client_ip": "", "session_id": ""}, "headers": {"host": "", "origin": "", "upgrade": "", "connection": "", "cookie": "", "pragma": "", "cache_control": "", "user_agent": "", "sec_websocket_version": "", "sec_websocket_key": "", "sec_websocket_extensions": "", "accept_encoding": "", "accept_language": "", "raw_headers": {}}, "page": {"host": "", "path": "", "raw_path": "", "full_path": "", "full_raw_path": "", "params": {}}, "url": {"scheme": "", "netloc": "", "origin": "://", "path": "", "query": "", "query_parameters": {}, "fragment": "", "href": ""}, "route_id": ""}}, "reflex___state____state.back_end___access___states___auth_state____auth_state": {"error_message_rx_state_": "", "session_token_rx_state_": ""}, "reflex___state____state.back_end___interface___state___dashboard_state____dashboard_state": {"eixos_resumo_rx_state_": [], "error_message_rx_state_": "", "loading_rx_state_": false, "metas_atingidas_rx_state_": 0, "metas_ativas_rx_state_": 0, "metas_com_empenho_rx_state_": 0, "metas_com_liquidacao_rx_state_": 0, "metas_com_previsao_rx_state_": 0, "metas_em_planejamento_rx_state_": 0, "metas_em_progresso_rx_state_": 0, "metas_por_eixo_rx_state_": [], "orcamento_empenhado_rx_state_": "R$ 0,00", "orcamento_liquidado_rx_state_": "R$ 0,00", "orcamento_previsao_rx_state_": "R$ 0,00", "percentual_atingidas_rx_state_": 0.0, "percentual_em_planejamento_rx_state_": 0.0, "percentual_em_progresso_rx_state_": 0.0, "percentual_empenhado_rx_state_": 0.0, "percentual_liquidado_rx_state_": 0.0, "prazo_resumo_rx_state_": [], "situacao_resumo_rx_state_": [], "sync_message_rx_state_": "", "total_metas_rx_state_": 0, "total_temas_rx_state_": 0, "ultima_sincronizacao_rx_state_": "Sem atualização"}, "reflex___state____state.back_end___interface___state___meta___meta_detail_state____meta_detail_state": {"andamento_rx_state_": "", "codigo_atual_rx_state_": "", "contexto_rx_state_": "", "eixo_rx_state_": "", "empenhado_rx_state_": "Não informado", "error_message_rx_state_": "", "ficha_encontrada_rx_state_": false, "iniciativas_rx_state_": [], "liquidado_rx_state_": "Não informado", "loading_rx_state_": true, "ods_rx_state_": [], "orgaos_rx_state_": [], "prazo_rx_state_": "", "previsao_rx_state_": "Não informado", "situacao_rx_state_": "", "titulo_rx_state_": ""}, "reflex___state____state.back_end___interface___state___sidebar_state____sidebar_state": {"expanded_rx_state_": true}, "reflex___state____state.reflex___istate___shared____shared_state_base_internal": {}, "reflex___state____state.reflex___state____frontend_event_exception_state": {}, "reflex___state____state.reflex___state____on_load_internal_state": {}, "reflex___state____state.reflex___state____update_vars_internal_state": {}}

export const defaultColorMode = "system"
export const ColorModeContext = createContext({
  colorMode: defaultColorMode,
  resolvedColorMode: defaultColorMode === "dark" ? "dark" : "light",
  toggleColorMode: () => {},
  setColorMode: () => {},
});
export const UploadFilesContext = createContext(null);
export const DispatchContext = createContext(null);
export const StateContexts = {reflex___state____state: createContext(null),reflex___state____state__back_end___access___states___auth_state____auth_state: createContext(null),reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state: createContext(null),reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state: createContext(null),reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state: createContext(null),reflex___state____state__reflex___istate___shared____shared_state_base_internal: createContext(null),reflex___state____state__reflex___state____frontend_event_exception_state: createContext(null),reflex___state____state__reflex___state____on_load_internal_state: createContext(null),reflex___state____state__reflex___state____update_vars_internal_state: createContext(null),};
export const EventLoopContext = createContext(null);
export const clientStorage = {"cookies": {"reflex___state____state.back_end___access___states___auth_state____auth_state.session_token_rx_state_": {"name": "pdm_session", "path": "/", "maxAge": 28800, "secure": false, "sameSite": "strict"}}, "local_storage": {}, "session_storage": {}}


export const state_name = "reflex___state____state"

export const exception_state_name = "reflex___state____state.reflex___state____frontend_event_exception_state"

// These events are triggered on initial load and each page navigation.
export const onLoadInternalEvent = () => {
    const internal_events = [];

    // Get tracked cookie and local storage vars to send to the backend.
    const client_storage_vars = hydrateClientStorage(clientStorage);
    // But only send the vars if any are actually set in the browser.
    if (client_storage_vars && Object.keys(client_storage_vars).length !== 0) {
        internal_events.push(
            ReflexEvent(
                'reflex___state____state.reflex___state____update_vars_internal_state.update_vars_internal',
                {vars: client_storage_vars},
            ),
        );
    }

    // `on_load_internal` triggers the correct on_load event(s) for the current page.
    // If the page does not define any on_load event, this will just set `is_hydrated = true`.
    internal_events.push(ReflexEvent('reflex___state____state.reflex___state____on_load_internal_state.on_load_internal'));

    return internal_events;
}

// The following events are sent when the websocket connects or reconnects.
export const initialEvents = () => [
    ReflexEvent('reflex___state____state.hydrate'),
    ...onLoadInternalEvent()
]
    

export const isDevMode = true;

// Module-level event dispatchers populated by ``EventLoopProvider`` on each
// render. Components reach addEvents/connectErrors via this import instead of
// hoisting ``useContext(EventLoopContext)`` so JSX literals (e.g.
// ``ErrorBoundary.onError``) constructed in any JS scope can dispatch events
// without depending on lexical hook hoisting.
let _addEventsImpl = (events, args, event_actions) => {
  console.warn("addEvents called before EventLoopProvider mounted", events);
};
let _connectErrorsImpl = [];

export function addEvents(events, args, event_actions) {
  return _addEventsImpl(events, args, event_actions);
}

export function getConnectErrors() {
  return _connectErrorsImpl;
}

export function UploadFilesProvider({ children }) {
  const [filesById, setFilesById] = useState({})
  refs["__clear_selected_files"] = (id) => setFilesById(filesById => {
    const newFilesById = {...filesById}
    delete newFilesById[id]
    return newFilesById
  })
  return createElement(
    UploadFilesContext.Provider,
    { value: [filesById, setFilesById] },
    children
  );
}

export function ClientSide(component) {
  return ({ children, ...props }) => {
    const [Component, setComponent] = useState(null);
    useEffect(() => {
      async function load() {
        const comp = await component();
        setComponent(() => comp);
      }
      load();
    }, []);
    return Component ? jsx(Component, props, children) : null;
  };
}

export function EventLoopProvider({ children }) {
  const dispatch = useContext(DispatchContext)
  const [addEventsLocal, connectErrors] = useEventLoop(
    dispatch,
    initialEvents,
    clientStorage,
  )
  // Populate the module-level dispatchers so JSX literals constructed
  // outside the React-tree path (e.g. ``ErrorBoundary.onError``) can call
  // ``addEvents`` without needing the events hook hoisted in their scope.
  _addEventsImpl = addEventsLocal;
  _connectErrorsImpl = connectErrors;
  return createElement(
    EventLoopContext.Provider,
    { value: [addEventsLocal, connectErrors] },
    children
  );
}

export function StateProvider({ children }) {
  const [reflex___state____state, dispatch_reflex___state____state] = useReducer(applyDelta, initialState["reflex___state____state"])
const [reflex___state____state__back_end___access___states___auth_state____auth_state, dispatch_reflex___state____state__back_end___access___states___auth_state____auth_state] = useReducer(applyDelta, initialState["reflex___state____state.back_end___access___states___auth_state____auth_state"])
const [reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state, dispatch_reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state] = useReducer(applyDelta, initialState["reflex___state____state.back_end___interface___state___dashboard_state____dashboard_state"])
const [reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state, dispatch_reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state] = useReducer(applyDelta, initialState["reflex___state____state.back_end___interface___state___meta___meta_detail_state____meta_detail_state"])
const [reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state, dispatch_reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state] = useReducer(applyDelta, initialState["reflex___state____state.back_end___interface___state___sidebar_state____sidebar_state"])
const [reflex___state____state__reflex___istate___shared____shared_state_base_internal, dispatch_reflex___state____state__reflex___istate___shared____shared_state_base_internal] = useReducer(applyDelta, initialState["reflex___state____state.reflex___istate___shared____shared_state_base_internal"])
const [reflex___state____state__reflex___state____frontend_event_exception_state, dispatch_reflex___state____state__reflex___state____frontend_event_exception_state] = useReducer(applyDelta, initialState["reflex___state____state.reflex___state____frontend_event_exception_state"])
const [reflex___state____state__reflex___state____on_load_internal_state, dispatch_reflex___state____state__reflex___state____on_load_internal_state] = useReducer(applyDelta, initialState["reflex___state____state.reflex___state____on_load_internal_state"])
const [reflex___state____state__reflex___state____update_vars_internal_state, dispatch_reflex___state____state__reflex___state____update_vars_internal_state] = useReducer(applyDelta, initialState["reflex___state____state.reflex___state____update_vars_internal_state"])
  const dispatchers = useMemo(() => {
    return {
      "reflex___state____state": dispatch_reflex___state____state,
"reflex___state____state.back_end___access___states___auth_state____auth_state": dispatch_reflex___state____state__back_end___access___states___auth_state____auth_state,
"reflex___state____state.back_end___interface___state___dashboard_state____dashboard_state": dispatch_reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state,
"reflex___state____state.back_end___interface___state___meta___meta_detail_state____meta_detail_state": dispatch_reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state,
"reflex___state____state.back_end___interface___state___sidebar_state____sidebar_state": dispatch_reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state,
"reflex___state____state.reflex___istate___shared____shared_state_base_internal": dispatch_reflex___state____state__reflex___istate___shared____shared_state_base_internal,
"reflex___state____state.reflex___state____frontend_event_exception_state": dispatch_reflex___state____state__reflex___state____frontend_event_exception_state,
"reflex___state____state.reflex___state____on_load_internal_state": dispatch_reflex___state____state__reflex___state____on_load_internal_state,
"reflex___state____state.reflex___state____update_vars_internal_state": dispatch_reflex___state____state__reflex___state____update_vars_internal_state,
    }
  }, [])

  return (
    createElement(StateContexts.reflex___state____state,{value: reflex___state____state},
createElement(StateContexts.reflex___state____state__back_end___access___states___auth_state____auth_state,{value: reflex___state____state__back_end___access___states___auth_state____auth_state},
createElement(StateContexts.reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state,{value: reflex___state____state__back_end___interface___state___dashboard_state____dashboard_state},
createElement(StateContexts.reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state,{value: reflex___state____state__back_end___interface___state___meta___meta_detail_state____meta_detail_state},
createElement(StateContexts.reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state,{value: reflex___state____state__back_end___interface___state___sidebar_state____sidebar_state},
createElement(StateContexts.reflex___state____state__reflex___istate___shared____shared_state_base_internal,{value: reflex___state____state__reflex___istate___shared____shared_state_base_internal},
createElement(StateContexts.reflex___state____state__reflex___state____frontend_event_exception_state,{value: reflex___state____state__reflex___state____frontend_event_exception_state},
createElement(StateContexts.reflex___state____state__reflex___state____on_load_internal_state,{value: reflex___state____state__reflex___state____on_load_internal_state},
createElement(StateContexts.reflex___state____state__reflex___state____update_vars_internal_state,{value: reflex___state____state__reflex___state____update_vars_internal_state},
    createElement(DispatchContext, {value: dispatchers}, children)
    )))))))))
  )
}