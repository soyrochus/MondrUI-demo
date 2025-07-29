
There is a new open-source Python library called NiceGUI. With NiceGUI you can write graphical user interfaces which run in the browser. It has a very gentle learning curve while still offering the option for advanced customizations. NiceGUI follows a backend-first philosophy: it handles all the web development details for you. You can focus on writing Python code. This makes it ideal for a wide range of projects including short scripts, dashboards, robotics projects, IoT solutions, smart home automation, and machine learning. Here is a short fully functional code example main.py:

```py
from nicegui import ui
ui.button('Click me', on_click=lambda: ui.notify(‘clicked’))
ui.run()
```

Install with “pip install nicegui” and launch “python3 main.py”; it will open a new tab in your browser showing a button that when clicked, displays a snackbar notification.

NiceGUI was initially built for accessing and controlling hardware like gpios, leds or usb devices. Over time it grew greatly beyond that. For example the website https://nicegui.io/ is itself running with NiceGUI. And with native mode, NiceGUI has Electron-like capabilities.
Unlike Streamlit the framework took much care to allow easy integration with any other Python libraries.
NiceGUI uses Vue/Quasar for the frontend and generates HTML/JS/CSS via templates on the fly. The backend is build on top FastAPI and uses socket.io for fast communication with the frontend. All user interactions are send to the backend and invoke the proper Python functions. Thereby it works best when there is a fast enough internet connection. Therefore is not meant to replace classical web apps; its main purpose is a quick way to build user interfaces for your Python code.

# Main Features

**Interaction:**
buttons, switches, sliders, inputs, ...
notifications, dialogs and menus
keyboard input
on-screen joystick

**Layout:**
navigation bars, tabs, panels, ...
grouping with rows, columns and cards
HTML and Markdown elements
flex layout by default

**Visualization:**
charts, diagrams and tables
3D scenes
progress bars
built-in timer for data refresh

**Styling:**
customizable color themes
custom CSS and classes
modern look with material design
built-in Tailwind support

**Coding:**
live-cycle events
implicit reload on code change (thanks to uvicorn)
straight-forward data binding
execute javascript from Python

**Foundation:**
generic Vue to Python bridge
dynamic GUI through Quasar
content is served with FastAPI
Python 3.8+

# Technical Details
NiceGUI only uses one uvicorn worker (to not have to implement/support tricky synchronization).
The socket.io library is used for managing web sockets. After the initial content is loaded a web socket connection is established and kept open for communication as long as the web page is shown. Each http request gets its own web socket connection.

See down for the documentation set: 

[
  {
    "title": "Read and write to the clipboard: Read and write to the clipboard",
    "content": "The following demo shows how to use `ui.clipboard.read()`, `ui.clipboard.write()` and `ui.clipboard.read_image()` to interact with the clipboard.\n\nBecause auto-index page can be accessed by multiple browser tabs simultaneously, reading the clipboard is not supported on this page.\nThis is only possible within page-builder functions decorated with `ui.page`, as shown in this demo.\n\nNote that your browser may ask for permission to access the clipboard or may not support this feature at all.",
    "format": "md",
    "demo": "from nicegui import ui\n\n@ui.page('/')\nasync def index():\n    ui.button('Write Text', on_click=lambda: ui.clipboard.write('Hi!'))\n\n    async def read() -\u003E None:\n        ui.notify(await ui.clipboard.read())\n    ui.button('Read Text', on_click=read)\n\n    async def read_image() -\u003E None:\n        img = await ui.clipboard.read_image()\n        if not img:\n            ui.notify('You must copy an image to clipboard first.')\n        else:\n            image.set_source(img)\n    ui.button('Read Image', on_click=read_image)\n    image = ui.image().classes('w-72')\n\nui.run()",
    "url": "/documentation/clipboard#read_and_write_to_the_clipboard"
  },
  {
    "title": "Read and write to the clipboard: Client-side clipboard",
    "content": "In order to avoid the round-trip to the server, you can also use the client-side clipboard API directly.\nThis might be supported by more browsers because the clipboard access is directly triggered by a user action.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.button('Write').on('click', js_handler='''\n    () =\u003E navigator.clipboard.writeText(\"Ho!\")\n''')\nui.button('Read').on('click', js_handler='''\n    async () =\u003E emitEvent(\"clipboard\", await navigator.clipboard.readText())\n''')\nui.on('clipboard', lambda e: ui.notify(e.args))\n\nui.run()",
    "url": "/documentation/clipboard#client-side_clipboard"
  },
  {
    "title": "Generic Events: Generic Events",
    "content": "Most UI elements come with predefined events.\nFor example, a `ui.button` like \"A\" in the demo has an `on_click` parameter that expects a coroutine or function.\nBut you can also use the `on` method to register a generic event handler like for \"B\".\nThis allows you to register handlers for any event that is supported by JavaScript and Quasar.\n\nFor example, you can register a handler for the `mousemove` event like for \"C\", even though there is no `on_mousemove` parameter for `ui.button`.\nSome events, like `mousemove`, are fired very often.\nTo avoid performance issues, you can use the `throttle` parameter to only call the handler every `throttle` seconds (\"D\").\n\nThe generic event handler can be synchronous or asynchronous and optionally takes `GenericEventArguments` as argument (\"E\").\nYou can also specify which attributes of the JavaScript or Quasar event should be passed to the handler (\"F\").\nThis can reduce the amount of data that needs to be transferred between the server and the client.\n\nHere you can find more information about the events that are supported:\n\n- \u003Chttps://developer.mozilla.org/en-US/docs/Web/API/HTMLElement#events\u003E for HTML elements\n- \u003Chttps://quasar.dev/vue-components\u003E for Quasar-based elements (see the \"Events\" tab on the individual component page)",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.row():\n    ui.button('A', on_click=lambda: ui.notify('You clicked the button A.'))\n    ui.button('B').on('click', lambda: ui.notify('You clicked the button B.'))\nwith ui.row():\n    ui.button('C').on('mousemove', lambda: ui.notify('You moved on button C.'))\n    ui.button('D').on('mousemove', lambda: ui.notify('You moved on button D.'), throttle=0.5)\nwith ui.row():\n    ui.button('E').on('mousedown', lambda e: ui.notify(e))\n    ui.button('F').on('mousedown', lambda e: ui.notify(e), ['ctrlKey', 'shiftKey'])\n\nui.run()",
    "url": "/documentation/generic_events#generic_events"
  },
  {
    "title": "Generic Events: Specifying event attributes",
    "content": "**A list of strings** names the attributes of the JavaScript event object:\n```py\nui.button().on('click', handle_click, ['clientX', 'clientY'])\n```\n\n**An empty list** requests _no_ attributes:\n```py\nui.button().on('click', handle_click, [])\n```\n\n**The value `None`** represents _all_ attributes (the default):\n```py\nui.button().on('click', handle_click, None)\n```\n\n**If the event is called with multiple arguments** like QTable's \"row-click\" `(evt, row, index) =\u003E void`,\nyou can define a list of argument definitions:\n```py\nui.table(...).on('rowClick', handle_click, [[], ['name'], None])\n```\nIn this example the \"row-click\" event will omit all arguments of the first `evt` argument,\nsend only the \"name\" attribute of the `row` argument and send the full `index`.\n\nIf the retrieved list of event arguments has length 1, the argument is automatically unpacked.\nSo you can write\n```py\nui.button().on('click', lambda e: print(e.args['clientX'], flush=True))\n```\ninstead of\n```py\nui.button().on('click', lambda e: print(e.args[0]['clientX'], flush=True))\n```\n\nNote that by default all JSON-serializable attributes of all arguments are sent.\nThis is to simplify registering for new events and discovering their attributes.\nIf bandwidth is an issue, the arguments should be limited to what is actually needed on the server.",
    "format": "md",
    "demo": "from nicegui import ui\n\ncolumns = [\n    {'name': 'name', 'label': 'Name', 'field': 'name'},\n    {'name': 'age', 'label': 'Age', 'field': 'age'},\n]\nrows = [\n    {'name': 'Alice', 'age': 42},\n    {'name': 'Bob', 'age': 23},\n]\nui.table(columns=columns, rows=rows, row_key='name') \\\n    .on('rowClick', ui.notify, [[], ['name'], None])\n\nui.run()",
    "url": "/documentation/generic_events#specifying_event_attributes"
  },
  {
    "title": "Generic Events: Modifiers",
    "content": "You can also include [key modifiers](https://vuejs.org/guide/essentials/event-handling.html#key-modifiers\u003E) (shown in input \"A\"),\nmodifier combinations (shown in input \"B\"),\nand [event modifiers](https://vuejs.org/guide/essentials/event-handling.html#mouse-button-modifiers\u003E) (shown in input \"C\").",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.row():\n    ui.input('A').classes('w-12').on('keydown.space', lambda: ui.notify('You pressed space.'))\n    ui.input('B').classes('w-12').on('keydown.y.shift', lambda: ui.notify('You pressed Shift+Y'))\n    ui.input('C').classes('w-12').on('keydown.once', lambda: ui.notify('You started typing.'))\n\nui.run()",
    "url": "/documentation/generic_events#modifiers"
  },
  {
    "title": "Generic Events: Custom events",
    "content": "It is fairly easy to emit custom events from JavaScript with `emitEvent(...)` which can be listened to with `ui.on(...)`.\nThis can be useful if you want to call Python code when something happens in JavaScript.\nIn this example we are listening to the `visibilitychange` event of the browser tab.",
    "format": "md",
    "demo": "from nicegui import ui\n\ntabwatch = ui.checkbox('Watch browser tab re-entering')\nui.on('tabvisible', lambda: ui.notify('Welcome back!') if tabwatch.value else None)\nui.add_head_html('''\n    \u003Cscript\u003E\n    document.addEventListener('visibilitychange', () =\u003E {\n        if (document.visibilityState === 'visible') {\n            emitEvent('tabvisible');\n        }\n    });\n    \u003C/script\u003E\n''')\n\nui.run()",
    "url": "/documentation/generic_events#custom_events"
  },
  {
    "title": "Generic Events: Pure JavaScript events",
    "content": "You can also use the `on` method to register a pure JavaScript event handler.\nThis can be useful if you want to call JavaScript code without sending any data to the server.\nIn this example we are using the `navigator.clipboard` API to copy a string to the clipboard.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.button('Copy to clipboard') \\\n    .on('click', js_handler='''() =\u003E {\n        navigator.clipboard.writeText(\"Hello, NiceGUI!\");\n    }''')\n\nui.run()",
    "url": "/documentation/generic_events#pure_javascript_events"
  },
  {
    "title": "ui.keyboard: Keyboard",
    "content": "Adds global keyboard event tracking.\n\nThe ``on_key`` callback receives a ``KeyEventArguments`` object with the following attributes:\n\n- ``sender``: the ``Keyboard`` element\n- ``client``: the client object\n- ``action``: a ``KeyboardAction`` object with the following attributes:\n    - ``keydown``: whether the key was pressed\n    - ``keyup``: whether the key was released\n    - ``repeat``: whether the key event was a repeat\n- ``key``: a ``KeyboardKey`` object with the following attributes:\n    - ``name``: the name of the key (e.g. \"a\", \"Enter\", \"ArrowLeft\"; see `here \u003Chttps://developer.mozilla.org/en-US/docs/Web/API/UI_Events/Keyboard_event_key_values\u003E`_ for a list of possible values)\n    - ``code``: the code of the key (e.g. \"KeyA\", \"Enter\", \"ArrowLeft\")\n    - ``location``: the location of the key (0 for standard keys, 1 for left keys, 2 for right keys, 3 for numpad keys)\n- ``modifiers``: a ``KeyboardModifiers`` object with the following attributes:\n    - ``alt``: whether the alt key was pressed\n    - ``ctrl``: whether the ctrl key was pressed\n    - ``meta``: whether the meta key was pressed\n    - ``shift``: whether the shift key was pressed\n\nFor convenience, the ``KeyboardKey`` object also has the following properties:\n    - ``is_cursorkey``: whether the key is a cursor (arrow) key\n    - ``number``: the integer value of a number key (0-9, ``None`` for other keys)\n    - ``backspace``, ``tab``, ``enter``, ``shift``, ``control``, ``alt``, ``pause``, ``caps_lock``, ``escape``, ``space``,\n      ``page_up``, ``page_down``, ``end``, ``home``, ``arrow_left``, ``arrow_up``, ``arrow_right``, ``arrow_down``,\n      ``print_screen``, ``insert``, ``delete``, ``meta``,\n      ``f1``, ``f2``, ``f3``, ``f4``, ``f5``, ``f6``, ``f7``, ``f8``, ``f9``, ``f10``, ``f11``, ``f12``: whether the key is the respective key\n\n:param on_key: callback to be executed when keyboard events occur.\n:param active: boolean flag indicating whether the callback should be executed or not (default: ``True``)\n:param repeating: boolean flag indicating whether held keys should be sent repeatedly (default: ``True``)\n:param ignore: ignore keys when one of these element types is focussed (default: ``['input', 'select', 'button', 'textarea']``)\n",
    "format": "rst",
    "demo": "from nicegui import ui\nfrom nicegui.events import KeyEventArguments\n\ndef handle_key(e: KeyEventArguments):\n    if e.key == 'f' and not e.action.repeat:\n        if e.action.keyup:\n            ui.notify('f was just released')\n        elif e.action.keydown:\n            ui.notify('f was just pressed')\n    if e.modifiers.shift and e.action.keydown:\n        if e.key.arrow_left:\n            ui.notify('going left')\n        elif e.key.arrow_right:\n            ui.notify('going right')\n        elif e.key.arrow_up:\n            ui.notify('going up')\n        elif e.key.arrow_down:\n            ui.notify('going down')\n\nkeyboard = ui.keyboard(on_key=handle_key)\nui.label('Key events can be caught globally by using the keyboard element.')\nui.checkbox('Track key events').bind_value_to(keyboard, 'active')\n\nui.run()",
    "url": "/documentation/keyboard#keyboard"
  },
  {
    "title": "ui.keyboard: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/keyboard#reference"
  },
  {
    "title": "ui.refreshable: Refreshable UI functions",
    "content": "The ``@ui.refreshable`` decorator allows you to create functions that have a ``refresh`` method.\nThis method will automatically delete all elements created by the function and recreate them.\n\nFor decorating refreshable methods in classes, there is a ``@ui.refreshable_method`` decorator,\nwhich is equivalent but prevents static type checking errors.\n",
    "format": "rst",
    "demo": "import random\nfrom nicegui import ui\n\nnumbers = []\n\n@ui.refreshable\ndef number_ui() -\u003E None:\n    ui.label(', '.join(str(n) for n in sorted(numbers)))\n\ndef add_number() -\u003E None:\n    numbers.append(random.randint(0, 100))\n    number_ui.refresh()\n\nnumber_ui()\nui.button('Add random number', on_click=add_number)\n\nui.run()",
    "url": "/documentation/refreshable#refreshable_ui_functions"
  },
  {
    "title": "ui.refreshable: Refreshable UI with parameters",
    "content": "Here is a demo of how to use the refreshable decorator to create a UI that can be refreshed with different parameters.",
    "format": "md",
    "demo": "import pytz\nfrom datetime import datetime\nfrom nicegui import ui\n\n@ui.refreshable\ndef clock_ui(timezone: str):\n    ui.label(f'Current time in {timezone}:')\n    ui.label(datetime.now(tz=pytz.timezone(timezone)).strftime('%H:%M:%S'))\n\nclock_ui('Europe/Berlin')\nui.button('Refresh', on_click=clock_ui.refresh)\nui.button('Refresh for New York', on_click=lambda: clock_ui.refresh('America/New_York'))\nui.button('Refresh for Tokyo', on_click=lambda: clock_ui.refresh('Asia/Tokyo'))\n\nui.run()",
    "url": "/documentation/refreshable#refreshable_ui_with_parameters"
  },
  {
    "title": "ui.refreshable: Refreshable UI for input validation",
    "content": "Here is a demo of how to use the refreshable decorator to give feedback about the validity of user input.",
    "format": "md",
    "demo": "import re\nfrom nicegui import ui\n\npwd = ui.input('Password', password=True, on_change=lambda: show_info.refresh())\n\nrules = {\n    'Lowercase letter': lambda s: re.search(r'[a-z]', s),\n    'Uppercase letter': lambda s: re.search(r'[A-Z]', s),\n    'Digit': lambda s: re.search(r'\\d', s),\n    'Special character': lambda s: re.search(r\"[!@#$%^&*(),.?':{}|\u003C\u003E]\", s),\n    'min. 8 characters': lambda s: len(s) \u003E= 8,\n}\n\n@ui.refreshable\ndef show_info():\n    for rule, check in rules.items():\n        with ui.row().classes('items-center gap-2'):\n            if check(pwd.value or ''):\n                ui.icon('done', color='green')\n                ui.label(rule).classes('text-xs text-green strike-through')\n            else:\n                ui.icon('radio_button_unchecked', color='red')\n                ui.label(rule).classes('text-xs text-red')\n\nshow_info()\n\nui.run()",
    "url": "/documentation/refreshable#refreshable_ui_for_input_validation"
  },
  {
    "title": "ui.refreshable: Refreshable UI with reactive state",
    "content": "You can create reactive state variables with the `ui.state` function, like `count` and `color` in this demo.\nThey can be used like normal variables for creating UI elements like the `ui.label`.\nTheir corresponding setter functions can be used to set new values, which will automatically refresh the UI.",
    "format": "md",
    "demo": "from nicegui import ui\n\n@ui.refreshable\ndef counter(name: str):\n    with ui.card():\n        count, set_count = ui.state(0)\n        color, set_color = ui.state('black')\n        ui.label(f'{name} = {count}').classes(f'text-{color}')\n        ui.button(f'{name} += 1', on_click=lambda: set_count(count + 1))\n        ui.select(['black', 'red', 'green', 'blue'],\n                  value=color, on_change=lambda e: set_color(e.value))\n\nwith ui.row():\n    counter('A')\n    counter('B')\n\nui.run()",
    "url": "/documentation/refreshable#refreshable_ui_with_reactive_state"
  },
  {
    "title": "ui.refreshable: Global scope",
    "content": "When defining a refreshable function in the global scope,\nevery refreshable UI that is created by calling this function will share the same state.\nIn this demo, `time()` will show the current date and time.\nWhen opening the page in a new tab, _both_ tabs will be updated simultaneously when clicking the \"Refresh\" button.\n\nSee the \"local scope\" demos below for a way to create independent refreshable UIs instead.",
    "format": "md",
    "demo": "from datetime import datetime\nfrom nicegui import ui\n\n@ui.refreshable\ndef time():\n    ui.label(f'Time: {datetime.now()}')\n\n@ui.page('/global_refreshable')\ndef demo():\n    time()\n    ui.button('Refresh', on_click=time.refresh)\n\nui.link('Open demo', demo)\n\nui.run()",
    "url": "/documentation/refreshable#global_scope"
  },
  {
    "title": "ui.refreshable: Local scope (variant A)",
    "content": "When defining a refreshable function in a local scope,\nrefreshable UI that is created by calling this function will refresh independently.\nIn contrast to the \"global scope\" demo,\nthe time will be updated only in the tab where the \"Refresh\" button was clicked.",
    "format": "md",
    "demo": "from datetime import datetime\nfrom nicegui import ui\n\n@ui.page('/local_refreshable_a')\ndef demo():\n    @ui.refreshable\n    def time():\n        ui.label(f'Time: {datetime.now()}')\n\n    time()\n    ui.button('Refresh', on_click=time.refresh)\n\nui.link('Open demo', demo)\n\nui.run()",
    "url": "/documentation/refreshable#local_scope_(variant_a)"
  },
  {
    "title": "ui.refreshable: Local scope (variant B)",
    "content": "In order to define refreshable UIs with local state outside of page functions,\nyou can, e.g., define a class with a refreshable method.\nThis way, you can create multiple instances of the class with independent state,\nbecause the `ui.refreshable` decorator acts on the class instance rather than the class itself.",
    "format": "md",
    "demo": "from datetime import datetime\nfrom nicegui import ui\n\nclass Clock:\n    @ui.refreshable_method\n    def time(self):\n        ui.label(f'Time: {datetime.now()}')\n\n@ui.page('/local_refreshable_b')\ndef demo():\n    clock = Clock()\n    clock.time()\n    ui.button('Refresh', on_click=clock.time.refresh)\n\nui.link('Open demo', demo)\n\nui.run()",
    "url": "/documentation/refreshable#local_scope_(variant_b)"
  },
  {
    "title": "ui.refreshable: Local scope (variant C)",
    "content": "As an alternative to the class definition shown above, you can also define the UI function in global scope,\nbut apply the `ui.refreshable` decorator inside the page function.\nThis way the refreshable UI will refresh independently.",
    "format": "md",
    "demo": "from datetime import datetime\nfrom nicegui import ui\n\ndef time():\n    ui.label(f'Time: {datetime.now()}')\n\n@ui.page('/local_refreshable_c')\ndef demo():\n    refreshable_time = ui.refreshable(time)\n    refreshable_time()\n    ui.button('Refresh', on_click=refreshable_time.refresh)\n\nui.link('Open demo', demo)\n\nui.run()",
    "url": "/documentation/refreshable#local_scope_(variant_c)"
  },
  {
    "title": "ui.refreshable: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/refreshable#reference"
  },
  {
    "title": "ui.run_javascript: Run JavaScript",
    "content": "This function runs arbitrary JavaScript code on a page that is executed in the browser.\nThe client must be connected before this function is called.\nTo access a client-side Vue component or HTML element by ID,\nuse the JavaScript functions `getElement()` or `getHtmlElement()` (*added in version 2.9.0*).\n\nIf the function is awaited, the result of the JavaScript code is returned.\nOtherwise, the JavaScript code is executed without waiting for a response.\n\nNote that requesting data from the client is only supported for page functions, not for the shared auto-index page.\n\n:param code: JavaScript code to run\n:param timeout: timeout in seconds (default: `1.0`)\n\n:return: AwaitableResponse that can be awaited to get the result of the JavaScript code\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\n@ui.page('/')\ndef page():\n    def alert():\n        ui.run_javascript('alert(\"Hello!\")')\n\n    async def get_date():\n        time = await ui.run_javascript('Date()')\n        ui.notify(f'Browser time: {time}')\n\n    def access_elements():\n        ui.run_javascript(f'getHtmlElement({label.id}).innerText += \" Hello!\"')\n\n    ui.button('fire and forget', on_click=alert)\n    ui.button('receive result', on_click=get_date)\n    ui.button('access elements', on_click=access_elements)\n    label = ui.label()\n\nui.run()",
    "url": "/documentation/run_javascript#run_javascript"
  },
  {
    "title": "ui.run_javascript: Run async JavaScript",
    "content": "Using `run_javascript` you can also run asynchronous code in the browser.\nThe following demo shows how to get the current location of the user.",
    "format": "md",
    "demo": "from nicegui import ui\n\n@ui.page('/')\ndef page():\n    async def show_location():\n        response = await ui.run_javascript('''\n            return await new Promise((resolve, reject) =\u003E {\n                if (!navigator.geolocation) {\n                    reject(new Error('Geolocation is not supported by your browser'));\n                } else {\n                    navigator.geolocation.getCurrentPosition(\n                        (position) =\u003E {\n                            resolve({\n                                latitude: position.coords.latitude,\n                                longitude: position.coords.longitude,\n                            });\n                        },\n                        () =\u003E {\n                            reject(new Error('Unable to retrieve your location'));\n                        }\n                    );\n                }\n            });\n        ''', timeout=5.0)\n        ui.notify(f'Your location is {response[\"latitude\"]}, {response[\"longitude\"]}')\n\n    ui.button('Show location', on_click=show_location)\n\nui.run()",
    "url": "/documentation/run_javascript#run_async_javascript"
  },
  {
    "title": "Storage: Storage",
    "content": "NiceGUI offers a straightforward mechanism for data persistence within your application.\nIt features five built-in storage types:\n\n- `app.storage.tab`:\n    Stored server-side in memory, this dictionary is unique to each non-duplicated tab session and can hold arbitrary objects.\n    Data will be lost when restarting the server until \u003Chttps://github.com/zauberzeug/nicegui/discussions/2841\u003E is implemented.\n    This storage is only available within [page builder functions](/documentation/page)\n    and requires an established connection, obtainable via [`await client.connected()`](/documentation/page#wait_for_client_connection).\n- `app.storage.client`:\n    Also stored server-side in memory, this dictionary is unique to each client connection and can hold arbitrary objects.\n    Data will be discarded when the page is reloaded or the user navigates to another page.\n    Unlike data stored in `app.storage.tab` which can be persisted on the server even for days,\n    `app.storage.client` helps caching resource-hungry objects such as a streaming or database connection you need to keep alive\n    for dynamic site updates but would like to discard as soon as the user leaves the page or closes the browser.\n    This storage is only available within [page builder functions](/documentation/page).\n- `app.storage.user`:\n    Stored server-side, each dictionary is associated with a unique identifier held in a browser session cookie.\n    Unique to each user, this storage is accessible across all their browser tabs.\n    `app.storage.browser['id']` is used to identify the user.\n    This storage is only available within [page builder functions](/documentation/page)\n    and requires the `storage_secret` parameter in`ui.run()` to sign the browser session cookie.\n- `app.storage.general`:\n    Also stored server-side, this dictionary provides a shared storage space accessible to all users.\n- `app.storage.browser`:\n    Unlike the previous types, this dictionary is stored directly as the browser session cookie, shared among all browser tabs for the same user.\n    However, `app.storage.user` is generally preferred due to its advantages in reducing data payload, enhancing security, and offering larger storage capacity.\n    By default, NiceGUI holds a unique identifier for the browser session in `app.storage.browser['id']`.\n    This storage is only available within [page builder functions](/documentation/page)\n    and requires the `storage_secret` parameter in `ui.run()` to sign the browser session cookie.\n\nThe following table will help you to choose storage.\n\n| Storage type                | `client` | `tab`  | `browser` | `user` | `general` |\n|-----------------------------|----------|--------|-----------|--------|-----------|\n| Location                    | Server   | Server | Browser   | Server | Server    |\n| Across tabs                 | No       | No     | Yes       | Yes    | Yes       |\n| Across browsers             | No       | No     | No        | No     | Yes       |\n| Across server restarts      | No       | Yes    | No        | Yes    | Yes       |\n| Across page reloads         | No       | Yes    | Yes       | Yes    | Yes       |\n| Needs page builder function | Yes      | Yes    | Yes       | Yes    | No        |\n| Needs client connection     | No       | Yes    | No        | No     | No        |\n| Write only before response  | No       | No     | Yes       | No     | No        |\n| Needs serializable data     | No       | No     | Yes       | Yes    | Yes       |\n| Needs `storage_secret`      | No       | No     | Yes       | Yes    | No        |",
    "format": "md",
    "demo": "from nicegui import app, ui\n\n@ui.page('/')\ndef index():\n    app.storage.user['count'] = app.storage.user.get('count', 0) + 1\n    with ui.row():\n       ui.label('your own page visits:')\n       ui.label().bind_text_from(app.storage.user, 'count')\n\nui.run(storage_secret='private key to secure the browser session cookie')",
    "url": "/documentation/storage#storage"
  },
  {
    "title": "Storage: Counting page visits",
    "content": "Here we are using the automatically available browser-stored session ID to count the number of unique page visits.",
    "format": "md",
    "demo": "from collections import Counter\nfrom datetime import datetime\nfrom nicegui import app, ui\n\ncounter = Counter()\nstart = datetime.now().strftime('%H:%M, %d %B %Y')\n\n@ui.page('/')\ndef index():\n    counter[app.storage.browser['id']] += 1\n    ui.label(f'{len(counter)} unique views ({sum(counter.values())} overall) since {start}')\n\nui.run(storage_secret='private key to secure the browser session cookie')",
    "url": "/documentation/storage#counting_page_visits"
  },
  {
    "title": "Storage: Storing UI state",
    "content": "Storage can also be used in combination with [`bindings`](/documentation/section_binding_properties).\nHere we are storing the value of a textarea between visits.\nThe note is also shared between all tabs of the same user.",
    "format": "md",
    "demo": "from nicegui import app, ui\n\n@ui.page('/')\ndef index():\n    ui.textarea('This note is kept between visits') \\\n        .classes('w-full').bind_value(app.storage.user, 'note')\n\nui.run()",
    "url": "/documentation/storage#storing_ui_state"
  },
  {
    "title": "Storage: Storing data per browser tab",
    "content": "When storing data in `app.storage.tab`, a single user can open multiple tabs of the same app, each with its own storage data.\nThis may be beneficial in certain scenarios like search or when performing data analysis.\nIt is also more secure to use such a volatile storage for scenarios like logging into a bank account or accessing a password manager.",
    "format": "md",
    "demo": "from nicegui import app, ui\n\n@ui.page('/')\nasync def index():\n    await ui.context.client.connected()\n    app.storage.tab['count'] = app.storage.tab.get('count', 0) + 1\n    ui.label(f'Tab reloaded {app.storage.tab[\"count\"]} times')\n    ui.button('Reload page', on_click=ui.navigate.reload)\n\nui.run()",
    "url": "/documentation/storage#storing_data_per_browser_tab"
  },
  {
    "title": "Storage: Maximum age of tab storage",
    "content": "By default, the tab storage is kept for 30 days.\nYou can change this by setting `app.storage.max_tab_storage_age`.\n\n*Added in version 2.10.0*",
    "format": "md",
    "demo": "from datetime import timedelta\nfrom nicegui import app, ui\n\napp.storage.max_tab_storage_age = timedelta(minutes=1).total_seconds()\n\n@ui.page('/')\ndef index():\n   ui.label(f'Tab storage age: {app.storage.max_tab_storage_age} seconds')\n\nui.run()",
    "url": "/documentation/storage#maximum_age_of_tab_storage"
  },
  {
    "title": "Storage: Short-term memory",
    "content": "The goal of `app.storage.client` is to store data only for the duration of the current page visit.\nIn difference to data stored in `app.storage.tab`\n- which is persisted between page changes and even browser restarts as long as the tab is kept open -\nthe data in `app.storage.client` will be discarded if the user closes the browser, reloads the page or navigates to another page.\nThis is beneficial for resource-hungry, intentionally short-lived or sensitive data.\nAn example is a database connection, which should be closed as soon as the user leaves the page.\nAdditionally, this storage useful if you want to return a page with default settings every time a user reloads.\nMeanwhile, it keeps the data alive during in-page navigation.\nThis is also helpful when updating elements on the site at intervals, such as a live feed.",
    "format": "md",
    "demo": "from nicegui import app, ui\n\n@ui.page('/')\nasync def index():\n    cache = app.storage.client\n    cache['count'] = 0\n    ui.label().bind_text_from(cache, 'count', lambda n: f'Updated {n} times')\n    ui.button('Update content',\n              on_click=lambda: cache.update(count=cache['count'] + 1))\n    ui.button('Reload page', on_click=ui.navigate.reload)\n\nui.run()",
    "url": "/documentation/storage#short-term_memory"
  },
  {
    "title": "Storage: Indentation",
    "content": "\n    By default, the general and user storage data is stored in JSON format without indentation.\n    You can change this to an indentation of 2 spaces by setting\n    `app.storage.general.indent = True` or `app.storage.user.indent = True`.\n",
    "format": "md",
    "demo": "",
    "url": "/documentation/storage#indentation"
  },
  {
    "title": "Storage: Redis storage",
    "content": "\n    You can use [Redis](https://redis.io/) for storage as an alternative to the default file storage.\n    This is useful if you have multiple NiceGUI instances and want to share data across them.\n\n    To activate this feature install the `redis` package (`pip install nicegui[redis]`)\n    and provide the `NICEGUI_REDIS_URL` environment variable to point to your Redis server.\n    Our [Redis storage example](https://github.com/zauberzeug/nicegui/tree/main/examples/redis_storage) shows\n    how you can setup it up with a reverse proxy or load balancer.\n\n    Please note that the Redis sync always contains all the data, not only the changed values.\n\n    - For `app.storage.general` this is the whole dictionary.\n    - For `app.storage.user` it's all the data of the user.\n    - For `app.storage.tab` it's all the data stored for this specific tab.\n\n    If you have large data sets, we suggest to use a database instead.\n    See our [database example](https://github.com/zauberzeug/nicegui/blob/main/examples/sqlite_database/main.py) for a demo with SQLite.\n    But of course to sync between multiple instances you should replace SQLite with PostgreSQL or similar.\n\n    *Added in version 2.10.0*\n",
    "format": "md",
    "demo": "",
    "url": "/documentation/storage#redis_storage"
  },
  {
    "title": "ui.timer: Timer",
    "content": "One major drive behind the creation of NiceGUI was the necessity to have a simple approach to update the interface in regular intervals,\nfor example to show a graph with incoming measurements.\nA timer will execute a callback repeatedly with a given interval.\n\n:param interval: the interval in which the timer is called (can be changed during runtime)\n:param callback: function or coroutine to execute when interval elapses\n:param active: whether the callback should be executed or not (can be changed during runtime)\n:param once: whether the callback is only executed once after a delay specified by `interval` (default: `False`)\n:param immediate: whether the callback should be executed immediately (default: `True`, ignored if `once` is `True`, *added in version 2.9.0*)\n",
    "format": "rst",
    "demo": "from datetime import datetime\nfrom nicegui import ui\n\nlabel = ui.label()\nui.timer(1.0, lambda: label.set_text(f'{datetime.now():%X}'))\n\nui.run()",
    "url": "/documentation/timer#timer"
  },
  {
    "title": "ui.timer: Activate, deactivate and cancel a timer",
    "content": "You can activate and deactivate a timer using the `active` property.\nYou can cancel a timer using the `cancel` method.\nAfter canceling a timer, it cannot be activated anymore.",
    "format": "md",
    "demo": "from nicegui import ui\n\nslider = ui.slider(min=0, max=1, value=0.5)\ntimer = ui.timer(0.1, lambda: slider.set_value((slider.value + 0.01) % 1.0))\nui.switch('active').bind_value_to(timer, 'active')\nui.button('Cancel', on_click=timer.cancel)\n\nui.run()",
    "url": "/documentation/timer#activate__deactivate_and_cancel_a_timer"
  },
  {
    "title": "ui.timer: Call a function after a delay",
    "content": "You can call a function after a delay using a timer with the `once` parameter.",
    "format": "md",
    "demo": "from nicegui import ui\n\ndef handle_click():\n    ui.timer(1.0, lambda: ui.notify('Hi!'), once=True)\nui.button('Notify after 1 second', on_click=handle_click)\n\nui.run()",
    "url": "/documentation/timer#call_a_function_after_a_delay"
  },
  {
    "title": "ui.timer: Don't start immediately",
    "content": "By default, the timer will start immediately.\nYou can change this behavior by setting the `immediate` parameter to `False`.\nThis will delay the first execution of the callback by the given interval.\n\n*Added in version 2.9.0*",
    "format": "md",
    "demo": "from datetime import datetime\nfrom nicegui import ui\n\nlabel = ui.label()\nui.timer(1.0, lambda: label.set_text(f'{datetime.now():%X}'), immediate=False)\n\nui.run()",
    "url": "/documentation/timer#don_t_start_immediately"
  },
  {
    "title": "ui.timer: Global app timer",
    "content": "While `ui.timer` is kind of a UI element that runs in the context of the current page,\nyou can also use the global `app.timer` for UI-independent timers.\n\n*Added in version 2.9.0*",
    "format": "md",
    "demo": "from nicegui import app, ui\n\ncounter = {'value': 0}\napp.timer(1.0, lambda: counter.update(value=counter['value'] + 1))\n\n@ui.page('/')\ndef page():\n    ui.label().bind_text_from(counter, 'value', lambda value: f'Count: {value}')\n\nui.run()",
    "url": "/documentation/timer#global_app_timer"
  },
  {
    "title": "ui.timer: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/timer#reference"
  },
  {
    "title": "Action & Events: Timer",
    "content": "One major drive behind the creation of NiceGUI was the necessity to have a simple approach to update the interface in regular intervals,\nfor example to show a graph with incoming measurements.\nA timer will execute a callback repeatedly with a given interval.\n\n:param interval: the interval in which the timer is called (can be changed during runtime)\n:param callback: function or coroutine to execute when interval elapses\n:param active: whether the callback should be executed or not (can be changed during runtime)\n:param once: whether the callback is only executed once after a delay specified by `interval` (default: `False`)\n:param immediate: whether the callback should be executed immediately (default: `True`, ignored if `once` is `True`, *added in version 2.9.0*)\n",
    "format": "rst",
    "demo": "from datetime import datetime\nfrom nicegui import ui\n\nlabel = ui.label()\nui.timer(1.0, lambda: label.set_text(f'{datetime.now():%X}'))\n\nui.run()",
    "url": "/documentation/section_action_events#timer"
  },
  {
    "title": "Action & Events: Keyboard",
    "content": "Adds global keyboard event tracking.\n\nThe ``on_key`` callback receives a ``KeyEventArguments`` object with the following attributes:\n\n- ``sender``: the ``Keyboard`` element\n- ``client``: the client object\n- ``action``: a ``KeyboardAction`` object with the following attributes:\n    - ``keydown``: whether the key was pressed\n    - ``keyup``: whether the key was released\n    - ``repeat``: whether the key event was a repeat\n- ``key``: a ``KeyboardKey`` object with the following attributes:\n    - ``name``: the name of the key (e.g. \"a\", \"Enter\", \"ArrowLeft\"; see `here \u003Chttps://developer.mozilla.org/en-US/docs/Web/API/UI_Events/Keyboard_event_key_values\u003E`_ for a list of possible values)\n    - ``code``: the code of the key (e.g. \"KeyA\", \"Enter\", \"ArrowLeft\")\n    - ``location``: the location of the key (0 for standard keys, 1 for left keys, 2 for right keys, 3 for numpad keys)\n- ``modifiers``: a ``KeyboardModifiers`` object with the following attributes:\n    - ``alt``: whether the alt key was pressed\n    - ``ctrl``: whether the ctrl key was pressed\n    - ``meta``: whether the meta key was pressed\n    - ``shift``: whether the shift key was pressed\n\nFor convenience, the ``KeyboardKey`` object also has the following properties:\n    - ``is_cursorkey``: whether the key is a cursor (arrow) key\n    - ``number``: the integer value of a number key (0-9, ``None`` for other keys)\n    - ``backspace``, ``tab``, ``enter``, ``shift``, ``control``, ``alt``, ``pause``, ``caps_lock``, ``escape``, ``space``,\n      ``page_up``, ``page_down``, ``end``, ``home``, ``arrow_left``, ``arrow_up``, ``arrow_right``, ``arrow_down``,\n      ``print_screen``, ``insert``, ``delete``, ``meta``,\n      ``f1``, ``f2``, ``f3``, ``f4``, ``f5``, ``f6``, ``f7``, ``f8``, ``f9``, ``f10``, ``f11``, ``f12``: whether the key is the respective key\n\n:param on_key: callback to be executed when keyboard events occur.\n:param active: boolean flag indicating whether the callback should be executed or not (default: ``True``)\n:param repeating: boolean flag indicating whether held keys should be sent repeatedly (default: ``True``)\n:param ignore: ignore keys when one of these element types is focussed (default: ``['input', 'select', 'button', 'textarea']``)\n",
    "format": "rst",
    "demo": "from nicegui import ui\nfrom nicegui.events import KeyEventArguments\n\ndef handle_key(e: KeyEventArguments):\n    if e.key == 'f' and not e.action.repeat:\n        if e.action.keyup:\n            ui.notify('f was just released')\n        elif e.action.keydown:\n            ui.notify('f was just pressed')\n    if e.modifiers.shift and e.action.keydown:\n        if e.key.arrow_left:\n            ui.notify('going left')\n        elif e.key.arrow_right:\n            ui.notify('going right')\n        elif e.key.arrow_up:\n            ui.notify('going up')\n        elif e.key.arrow_down:\n            ui.notify('going down')\n\nkeyboard = ui.keyboard(on_key=handle_key)\nui.label('Key events can be caught globally by using the keyboard element.')\nui.checkbox('Track key events').bind_value_to(keyboard, 'active')\n\nui.run()",
    "url": "/documentation/section_action_events#keyboard"
  },
  {
    "title": "Action & Events: UI Updates",
    "content": "NiceGUI tries to automatically synchronize the state of UI elements with the client,\ne.g. when a label text, an input value or style/classes/props of an element have changed.\nIn other cases, you can explicitly call `element.update()` or `ui.update(*elements)` to update.\nThe demo code shows both methods for a `ui.echart`, where it is difficult to automatically detect changes in the `options` dictionary.",
    "format": "md",
    "demo": "from nicegui import ui\nfrom random import random\n\nchart = ui.echart({\n    'xAxis': {'type': 'value'},\n    'yAxis': {'type': 'value'},\n    'series': [{'type': 'line', 'data': [[0, 0], [1, 1]]}],\n})\n\ndef add():\n    chart.options['series'][0]['data'].append([random(), random()])\n    chart.update()\n\ndef clear():\n    chart.options['series'][0]['data'].clear()\n    ui.update(chart)\n\nwith ui.row():\n    ui.button('Add', on_click=add)\n    ui.button('Clear', on_click=clear)\n\nui.run()",
    "url": "/documentation/section_action_events#ui_updates"
  },
  {
    "title": "Action & Events: Refreshable UI functions",
    "content": "The ``@ui.refreshable`` decorator allows you to create functions that have a ``refresh`` method.\nThis method will automatically delete all elements created by the function and recreate them.\n\nFor decorating refreshable methods in classes, there is a ``@ui.refreshable_method`` decorator,\nwhich is equivalent but prevents static type checking errors.\n",
    "format": "rst",
    "demo": "import random\nfrom nicegui import ui\n\nnumbers = []\n\n@ui.refreshable\ndef number_ui() -\u003E None:\n    ui.label(', '.join(str(n) for n in sorted(numbers)))\n\ndef add_number() -\u003E None:\n    numbers.append(random.randint(0, 100))\n    number_ui.refresh()\n\nnumber_ui()\nui.button('Add random number', on_click=add_number)\n\nui.run()",
    "url": "/documentation/section_action_events#refreshable_ui_functions"
  },
  {
    "title": "Action & Events: Async event handlers",
    "content": "Most elements also support asynchronous event handlers.\n\nNote: You can also pass a `functools.partial` into the `on_click` property to wrap async functions with parameters.",
    "format": "md",
    "demo": "import asyncio\nfrom nicegui import ui\n\nasync def async_task():\n    ui.notify('Asynchronous task started')\n    await asyncio.sleep(5)\n    ui.notify('Asynchronous task finished')\n\nui.button('start async task', on_click=async_task)\n\nui.run()",
    "url": "/documentation/section_action_events#async_event_handlers"
  },
  {
    "title": "Action & Events: Generic Events",
    "content": "Most UI elements come with predefined events.\nFor example, a `ui.button` like \"A\" in the demo has an `on_click` parameter that expects a coroutine or function.\nBut you can also use the `on` method to register a generic event handler like for \"B\".\nThis allows you to register handlers for any event that is supported by JavaScript and Quasar.\n\nFor example, you can register a handler for the `mousemove` event like for \"C\", even though there is no `on_mousemove` parameter for `ui.button`.\nSome events, like `mousemove`, are fired very often.\nTo avoid performance issues, you can use the `throttle` parameter to only call the handler every `throttle` seconds (\"D\").\n\nThe generic event handler can be synchronous or asynchronous and optionally takes `GenericEventArguments` as argument (\"E\").\nYou can also specify which attributes of the JavaScript or Quasar event should be passed to the handler (\"F\").\nThis can reduce the amount of data that needs to be transferred between the server and the client.\n\nHere you can find more information about the events that are supported:\n\n- \u003Chttps://developer.mozilla.org/en-US/docs/Web/API/HTMLElement#events\u003E for HTML elements\n- \u003Chttps://quasar.dev/vue-components\u003E for Quasar-based elements (see the \"Events\" tab on the individual component page)",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.row():\n    ui.button('A', on_click=lambda: ui.notify('You clicked the button A.'))\n    ui.button('B').on('click', lambda: ui.notify('You clicked the button B.'))\nwith ui.row():\n    ui.button('C').on('mousemove', lambda: ui.notify('You moved on button C.'))\n    ui.button('D').on('mousemove', lambda: ui.notify('You moved on button D.'), throttle=0.5)\nwith ui.row():\n    ui.button('E').on('mousedown', lambda e: ui.notify(e))\n    ui.button('F').on('mousedown', lambda e: ui.notify(e), ['ctrlKey', 'shiftKey'])\n\nui.run()",
    "url": "/documentation/section_action_events#generic_events"
  },
  {
    "title": "Action & Events: Running CPU-bound tasks",
    "content": "NiceGUI provides a `cpu_bound` function for running CPU-bound tasks in a separate process.\nThis is useful for long-running computations that would otherwise block the event loop and make the UI unresponsive.\nThe function returns a future that can be awaited.\n\nNote:\nThe function needs to transfer the whole state of the passed function to the process, which is done with pickle.\nIt is encouraged to create free functions or static methods which get all the data as simple parameters (i.e. no class or UI logic)\nand return the result, instead of writing it in class properties or global variables.",
    "format": "md",
    "demo": "import time\nfrom nicegui import run, ui\n\ndef compute_sum(a: float, b: float) -\u003E float:\n    time.sleep(1)  # simulate a long-running computation\n    return a + b\n\nasync def handle_click():\n    result = await run.cpu_bound(compute_sum, 1, 2)\n    ui.notify(f'Sum is {result}')\n\nui.button('Compute', on_click=handle_click)\n\nui.run()",
    "url": "/documentation/section_action_events#running_cpu-bound_tasks"
  },
  {
    "title": "Action & Events: Running I/O-bound tasks",
    "content": "NiceGUI provides an `io_bound` function for running I/O-bound tasks in a separate thread.\nThis is useful for long-running I/O operations that would otherwise block the event loop and make the UI unresponsive.\nThe function returns a future that can be awaited.",
    "format": "md",
    "demo": "import httpx\nfrom nicegui import run, ui\n\nasync def handle_click():\n    URL = 'https://httpbin.org/delay/1'\n    response = await run.io_bound(httpx.get, URL, timeout=3)\n    ui.notify(f'Downloaded {len(response.content)} bytes')\n\nui.button('Download', on_click=handle_click)\n\nui.run()",
    "url": "/documentation/section_action_events#running_i_o-bound_tasks"
  },
  {
    "title": "Action & Events: Run JavaScript",
    "content": "This function runs arbitrary JavaScript code on a page that is executed in the browser.\nThe client must be connected before this function is called.\nTo access a client-side Vue component or HTML element by ID,\nuse the JavaScript functions `getElement()` or `getHtmlElement()` (*added in version 2.9.0*).\n\nIf the function is awaited, the result of the JavaScript code is returned.\nOtherwise, the JavaScript code is executed without waiting for a response.\n\nNote that requesting data from the client is only supported for page functions, not for the shared auto-index page.\n\n:param code: JavaScript code to run\n:param timeout: timeout in seconds (default: `1.0`)\n\n:return: AwaitableResponse that can be awaited to get the result of the JavaScript code\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\n@ui.page('/')\ndef page():\n    def alert():\n        ui.run_javascript('alert(\"Hello!\")')\n\n    async def get_date():\n        time = await ui.run_javascript('Date()')\n        ui.notify(f'Browser time: {time}')\n\n    def access_elements():\n        ui.run_javascript(f'getHtmlElement({label.id}).innerText += \" Hello!\"')\n\n    ui.button('fire and forget', on_click=alert)\n    ui.button('receive result', on_click=get_date)\n    ui.button('access elements', on_click=access_elements)\n    label = ui.label()\n\nui.run()",
    "url": "/documentation/section_action_events#run_javascript"
  },
  {
    "title": "Action & Events: Read and write to the clipboard",
    "content": "The following demo shows how to use `ui.clipboard.read()`, `ui.clipboard.write()` and `ui.clipboard.read_image()` to interact with the clipboard.\n\nBecause auto-index page can be accessed by multiple browser tabs simultaneously, reading the clipboard is not supported on this page.\nThis is only possible within page-builder functions decorated with `ui.page`, as shown in this demo.\n\nNote that your browser may ask for permission to access the clipboard or may not support this feature at all.",
    "format": "md",
    "demo": "from nicegui import ui\n\n@ui.page('/')\nasync def index():\n    ui.button('Write Text', on_click=lambda: ui.clipboard.write('Hi!'))\n\n    async def read() -\u003E None:\n        ui.notify(await ui.clipboard.read())\n    ui.button('Read Text', on_click=read)\n\n    async def read_image() -\u003E None:\n        img = await ui.clipboard.read_image()\n        if not img:\n            ui.notify('You must copy an image to clipboard first.')\n        else:\n            image.set_source(img)\n    ui.button('Read Image', on_click=read_image)\n    image = ui.image().classes('w-72')\n\nui.run()",
    "url": "/documentation/section_action_events#read_and_write_to_the_clipboard"
  },
  {
    "title": "Action & Events: Events",
    "content": "You can register coroutines or functions to be called for the following events:\n\n- `app.on_startup`: called when NiceGUI is started or restarted\n- `app.on_shutdown`: called when NiceGUI is shut down or restarted\n- `app.on_connect`: called for each client which connects (optional argument: nicegui.Client)\n- `app.on_disconnect`: called for each client which disconnects (optional argument: nicegui.Client)\n- `app.on_exception`: called when an exception occurs (optional argument: exception)\n\nWhen NiceGUI is shut down or restarted, all tasks still in execution will be automatically canceled.",
    "format": "md",
    "demo": "from datetime import datetime\nfrom nicegui import app, ui\n\ndt = datetime.now()\n\ndef handle_connection():\n    global dt\n    dt = datetime.now()\napp.on_connect(handle_connection)\n\nlabel = ui.label()\nui.timer(1, lambda: label.set_text(f'Last new connection: {dt:%H:%M:%S}'))\n\nui.run()",
    "url": "/documentation/section_action_events#events"
  },
  {
    "title": "Action & Events: Custom error page",
    "content": "You can use `@app.on_page_exception` to define a custom error page.\n\nThe handler must be a synchronous function that creates a page like a normal page function.\nIt can take the exception as an argument, but it is not required.\nIt overrides the default \"sad face\" error page, except when the error is re-raised.\n\nThe following example shows how to create a custom error page handler that only handles a specific exception.\nThe default error page handler is still used for all other exceptions.\n\nNote: Showing the traceback may not be a good idea in production, as it may leak sensitive information.\n\n*Added in version 2.20.0*",
    "format": "md",
    "demo": "import traceback\nfrom nicegui import app, ui\n\n@app.on_page_exception\ndef timeout_error_page(exception: Exception) -\u003E None:\n    if not isinstance(exception, TimeoutError):\n        raise exception\n    with ui.column().classes('absolute-center items-center gap-8'):\n        ui.icon('sym_o_timer', size='xl')\n        ui.label(f'{exception}').classes('text-2xl')\n        ui.code(traceback.format_exc(chain=False))\n\n@ui.page('/raise_timeout_error')\ndef raise_timeout_error():\n    raise TimeoutError('This took too long')\n\n@ui.page('/raise_runtime_error')\ndef raise_runtime_error():\n    raise RuntimeError('Something is wrong')\n\nui.link('Raise timeout error (custom error page)', '/raise_timeout_error')\nui.link('Raise runtime error (default error page)', '/raise_runtime_error')\n\nui.run()",
    "url": "/documentation/section_action_events#custom_error_page"
  },
  {
    "title": "Action & Events: Shut down NiceGUI",
    "content": "This will programmatically stop the server.\n",
    "format": "rst",
    "demo": "from nicegui import app, ui\n\nui.button('shutdown', on_click=app.shutdown)\n\nui.run(reload=False)",
    "url": "/documentation/section_action_events#shut_down_nicegui"
  },
  {
    "title": "Action & Events: Storage",
    "content": "NiceGUI offers a straightforward mechanism for data persistence within your application.\nIt features five built-in storage types:\n\n- `app.storage.tab`:\n    Stored server-side in memory, this dictionary is unique to each non-duplicated tab session and can hold arbitrary objects.\n    Data will be lost when restarting the server until \u003Chttps://github.com/zauberzeug/nicegui/discussions/2841\u003E is implemented.\n    This storage is only available within [page builder functions](/documentation/page)\n    and requires an established connection, obtainable via [`await client.connected()`](/documentation/page#wait_for_client_connection).\n- `app.storage.client`:\n    Also stored server-side in memory, this dictionary is unique to each client connection and can hold arbitrary objects.\n    Data will be discarded when the page is reloaded or the user navigates to another page.\n    Unlike data stored in `app.storage.tab` which can be persisted on the server even for days,\n    `app.storage.client` helps caching resource-hungry objects such as a streaming or database connection you need to keep alive\n    for dynamic site updates but would like to discard as soon as the user leaves the page or closes the browser.\n    This storage is only available within [page builder functions](/documentation/page).\n- `app.storage.user`:\n    Stored server-side, each dictionary is associated with a unique identifier held in a browser session cookie.\n    Unique to each user, this storage is accessible across all their browser tabs.\n    `app.storage.browser['id']` is used to identify the user.\n    This storage is only available within [page builder functions](/documentation/page)\n    and requires the `storage_secret` parameter in`ui.run()` to sign the browser session cookie.\n- `app.storage.general`:\n    Also stored server-side, this dictionary provides a shared storage space accessible to all users.\n- `app.storage.browser`:\n    Unlike the previous types, this dictionary is stored directly as the browser session cookie, shared among all browser tabs for the same user.\n    However, `app.storage.user` is generally preferred due to its advantages in reducing data payload, enhancing security, and offering larger storage capacity.\n    By default, NiceGUI holds a unique identifier for the browser session in `app.storage.browser['id']`.\n    This storage is only available within [page builder functions](/documentation/page)\n    and requires the `storage_secret` parameter in `ui.run()` to sign the browser session cookie.\n\nThe following table will help you to choose storage.\n\n| Storage type                | `client` | `tab`  | `browser` | `user` | `general` |\n|-----------------------------|----------|--------|-----------|--------|-----------|\n| Location                    | Server   | Server | Browser   | Server | Server    |\n| Across tabs                 | No       | No     | Yes       | Yes    | Yes       |\n| Across browsers             | No       | No     | No        | No     | Yes       |\n| Across server restarts      | No       | Yes    | No        | Yes    | Yes       |\n| Across page reloads         | No       | Yes    | Yes       | Yes    | Yes       |\n| Needs page builder function | Yes      | Yes    | Yes       | Yes    | No        |\n| Needs client connection     | No       | Yes    | No        | No     | No        |\n| Write only before response  | No       | No     | Yes       | No     | No        |\n| Needs serializable data     | No       | No     | Yes       | Yes    | Yes       |\n| Needs `storage_secret`      | No       | No     | Yes       | Yes    | No        |",
    "format": "md",
    "demo": "from nicegui import app, ui\n\n@ui.page('/')\ndef index():\n    app.storage.user['count'] = app.storage.user.get('count', 0) + 1\n    with ui.row():\n       ui.label('your own page visits:')\n       ui.label().bind_text_from(app.storage.user, 'count')\n\nui.run(storage_secret='private key to secure the browser session cookie')",
    "url": "/documentation/section_action_events#storage"
  },
  {
    "title": "ui.audio: Audio",
    "content": "Displays an audio player.\n\n:param src: URL or local file path of the audio source\n:param controls: whether to show the audio controls, like play, pause, and volume (default: `True`)\n:param autoplay: whether to start playing the audio automatically (default: `False`)\n:param muted: whether the audio should be initially muted (default: `False`)\n:param loop: whether the audio should loop (default: `False`)\n\nSee `here \u003Chttps://developer.mozilla.org/en-US/docs/Web/HTML/Element/audio#events\u003E`_\nfor a list of events you can subscribe to using the generic event subscription `on()`.\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\na = ui.audio('https://cdn.pixabay.com/download/audio/2022/02/22/audio_d1718ab41b.mp3')\na.on('ended', lambda _: ui.notify('Audio playback completed'))\n\nui.button(on_click=lambda: a.props('muted'), icon='volume_off').props('outline')\nui.button(on_click=lambda: a.props(remove='muted'), icon='volume_up').props('outline')\n\nui.run()",
    "url": "/documentation/audio#audio"
  },
  {
    "title": "ui.audio: Control the audio element",
    "content": "This demo shows how to play, pause and seek programmatically.",
    "format": "md",
    "demo": "from nicegui import ui\n\na = ui.audio('https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3')\nui.button('Play', on_click=a.play)\nui.button('Pause', on_click=a.pause)\nui.button('Jump to 0:30', on_click=lambda: a.seek(30))\n\nui.run()",
    "url": "/documentation/audio#control_the_audio_element"
  },
  {
    "title": "ui.audio: Event subscription",
    "content": "This demo shows how to subscribe to some of the [available events](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/audio#events).",
    "format": "md",
    "demo": "from nicegui import ui\n\na = ui.audio('https://cdn.pixabay.com/download/audio/2022/02/22/audio_d1718ab41b.mp3')\na.on('play', lambda _: ui.notify('Started'))\na.on('pause', lambda _: ui.notify('Paused'))\na.on('ended', lambda _: ui.notify('Completed'))\n\nui.run()",
    "url": "/documentation/audio#event_subscription"
  },
  {
    "title": "ui.audio: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/audio#reference"
  },
  {
    "title": "ui.avatar: Avatar",
    "content": "A avatar element wrapping Quasar's\n`QAvatar \u003Chttps://quasar.dev/vue-components/avatar\u003E`_ component.\n\n:param icon: name of the icon or image path with \"img:\" prefix (e.g. \"map\", \"img:path/to/image.png\")\n:param color: background color (either a Quasar, Tailwind, or CSS color or `None`, default: \"primary\")\n:param text_color: color name from the Quasar Color Palette (e.g. \"primary\", \"teal-10\")\n:param size: size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl) (e.g. \"16px\", \"2rem\")\n:param font_size: size in CSS units, including unit name, of the content (icon, text) (e.g. \"18px\", \"2rem\")\n:param square: removes border-radius so borders are squared (default: False)\n:param rounded: applies a small standard border-radius for a squared shape of the component (default: False)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.avatar('favorite_border', text_color='grey-11', square=True)\nui.avatar('img:https://nicegui.io/logo_square.png', color='blue-2')\n\nui.run()",
    "url": "/documentation/avatar#avatar"
  },
  {
    "title": "ui.avatar: Photos",
    "content": "To use a photo as an avatar, you can use `ui.image` within `ui.avatar`.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.avatar():\n    ui.image('https://robohash.org/robot?bgset=bg2')\n\nui.run()",
    "url": "/documentation/avatar#photos"
  },
  {
    "title": "ui.avatar: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/avatar#reference"
  },
  {
    "title": "ui.icon: Icon",
    "content": "This element is based on Quasar's `QIcon \u003Chttps://quasar.dev/vue-components/icon\u003E`_ component.\n\n`Here \u003Chttps://fonts.google.com/icons?icon.set=Material+Icons\u003E`_ is a reference of possible names.\n\n:param name: name of the icon (snake case, e.g. `add_circle`)\n:param size: size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl), examples: 16px, 2rem\n:param color: icon color (either a Quasar, Tailwind, or CSS color or `None`, default: `None`)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.icon('thumb_up', color='primary').classes('text-5xl')\n\nui.run()",
    "url": "/documentation/icon#icon"
  },
  {
    "title": "ui.icon: Material icons and symbols",
    "content": "You can use different sets of Material icons and symbols.\nThe [Quasar documentation](https://quasar.dev/vue-components/icon\\#webfont-usage)\ngives an overview of all available icon sets and their name prefix:\n\n* None for [filled icons](https://fonts.google.com/icons?icon.set=Material+Icons&icon.style=Filled)\n* \"o\\_\" for [outline icons](https://fonts.google.com/icons?icon.set=Material+Icons&icon.style=Outlined)\n* \"r\\_\" for [round icons](https://fonts.google.com/icons?icon.set=Material+Icons&icon.style=Rounded)\n* \"s\\_\" for [sharp icons](https://fonts.google.com/icons?icon.set=Material+Icons&icon.style=Sharp)\n* \"sym\\_o\\_\" for [outline symbols](https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Outlined)\n* \"sym\\_r\\_\" for [round symbols](https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Rounded)\n* \"sym\\_s\\_\" for [sharp symbols](https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Sharp)",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.row().classes('text-4xl'):\n    ui.icon('home')\n    ui.icon('o_home')\n    ui.icon('r_home')\n    ui.icon('sym_o_home')\n    ui.icon('sym_r_home')\n\nui.run()",
    "url": "/documentation/icon#material_icons_and_symbols"
  },
  {
    "title": "ui.icon: Eva icons",
    "content": "You can use [Eva icons](https://akveo.github.io/eva-icons/) in your app.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.add_head_html('\u003Clink href=\"https://unpkg.com/eva-icons@1.1.3/style/eva-icons.css\" rel=\"stylesheet\" /\u003E')\n\nui.icon('eva-github').classes('text-5xl')\n\nui.run()",
    "url": "/documentation/icon#eva_icons"
  },
  {
    "title": "ui.icon: Other icon sets",
    "content": "You can use the same approach for adding other icon sets to your app.\nAs a rule of thumb, you reference the corresponding CSS, and it in turn references font files.\nThis demo shows how to include [Themify icons](https://themify.me/themify-icons).",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.add_head_html('\u003Clink href=\"https://cdn.jsdelivr.net/themify-icons/0.1.2/css/themify-icons.css\" rel=\"stylesheet\" /\u003E')\n\nui.icon('ti-car').classes('text-5xl')\n\nui.run()",
    "url": "/documentation/icon#other_icon_sets"
  },
  {
    "title": "ui.icon: Lottie files",
    "content": "You can also use [Lottie files](https://lottiefiles.com/) with animations.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.add_body_html('\u003Cscript src=\"https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js\"\u003E\u003C/script\u003E')\n\nsrc = 'https://assets5.lottiefiles.com/packages/lf20_MKCnqtNQvg.json'\nui.html(f'\u003Clottie-player src=\"{src}\" loop autoplay /\u003E').classes('w-24')\n\nui.run()",
    "url": "/documentation/icon#lottie_files"
  },
  {
    "title": "ui.icon: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/icon#reference"
  },
  {
    "title": "ui.image: Image",
    "content": "Displays an image.\nThis element is based on Quasar's `QImg \u003Chttps://quasar.dev/vue-components/img\u003E`_ component.\n\n:param source: the source of the image; can be a URL, local file path, a base64 string or a PIL image\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.image('https://picsum.photos/id/377/640/360')\n\nui.run()",
    "url": "/documentation/image#image"
  },
  {
    "title": "ui.image: Local files",
    "content": "You can use local images as well by passing a path to the image file.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.image('website/static/logo.png').classes('w-16')\n\nui.run()",
    "url": "/documentation/image#local_files"
  },
  {
    "title": "ui.image: Base64 string",
    "content": "You can also use a Base64 string as image source.",
    "format": "md",
    "demo": "from nicegui import ui\n\nbase64 = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=='\nui.image(base64).classes('w-2 h-2 m-auto')\n\nui.run()",
    "url": "/documentation/image#base64_string"
  },
  {
    "title": "ui.image: PIL image",
    "content": "You can also use a PIL image as image source.",
    "format": "md",
    "demo": "import numpy as np\nfrom nicegui import ui\nfrom PIL import Image\n\nimage = Image.fromarray(np.random.randint(0, 255, (100, 100), dtype=np.uint8))\nui.image(image).classes('w-32')\n\nui.run()",
    "url": "/documentation/image#pil_image"
  },
  {
    "title": "ui.image: Lottie files",
    "content": "You can also use [Lottie files](https://lottiefiles.com/) with animations.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.add_body_html('\u003Cscript src=\"https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js\"\u003E\u003C/script\u003E')\n\nsrc = 'https://assets1.lottiefiles.com/datafiles/HN7OcWNnoqje6iXIiZdWzKxvLIbfeCGTmvXmEm1h/data.json'\nui.html(f'\u003Clottie-player src=\"{src}\" loop autoplay /\u003E').classes('w-full')\n\nui.run()",
    "url": "/documentation/image#lottie_files"
  },
  {
    "title": "ui.image: Image link",
    "content": "Images can link to another page by wrapping them in a [ui.link](https://nicegui.io/documentation/link).",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.link(target='https://github.com/zauberzeug/nicegui'):\n    ui.image('https://picsum.photos/id/41/640/360').classes('w-64')\n\nui.run()",
    "url": "/documentation/image#image_link"
  },
  {
    "title": "ui.image: Force reload",
    "content": "You can force an image to reload by calling the `force_reload` method.\nIt will append a timestamp to the image URL, which will make the browser reload the image.",
    "format": "md",
    "demo": "from nicegui import ui\n\nimg = ui.image('https://picsum.photos/640/360').classes('w-64')\n\nui.button('Force reload', on_click=img.force_reload)\n\nui.run()",
    "url": "/documentation/image#force_reload"
  },
  {
    "title": "ui.image: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/image#reference"
  },
  {
    "title": "ui.interactive_image: Interactive Image",
    "content": "Create an image with an SVG overlay that handles mouse events and yields image coordinates.\nIt is also the best choice for non-flickering image updates.\nIf the source URL changes faster than images can be loaded by the browser, some images are simply skipped.\nThereby repeatedly updating the image source will automatically adapt to the available bandwidth.\nSee `OpenCV Webcam \u003Chttps://github.com/zauberzeug/nicegui/tree/main/examples/opencv_webcam/main.py\u003E`_ for an example.\n\nThe mouse event handler is called with mouse event arguments containing\n\n- `type` (the name of the JavaScript event),\n- `image_x` and `image_y` (image coordinates in pixels),\n- `button` and `buttons` (mouse button numbers from the JavaScript event), as well as\n- `alt`, `ctrl`, `meta`, and `shift` (modifier keys from the JavaScript event).\n\nYou can also pass a tuple of width and height instead of an image source.\nThis will create an empty image with the given size.\n\n:param source: the source of the image; can be an URL, local file path, a base64 string or just an image size\n:param content: SVG content which should be overlaid; viewport has the same dimensions as the image\n:param size: size of the image (width, height) in pixels; only used if `source` is not set\n:param on_mouse: callback for mouse events (contains image coordinates `image_x` and `image_y` in pixels)\n:param events: list of JavaScript events to subscribe to (default: `['click']`)\n:param cross: whether to show crosshairs or a color string (default: `False`)\n",
    "format": "rst",
    "demo": "from nicegui import events, ui\n\ndef mouse_handler(e: events.MouseEventArguments):\n    color = 'SkyBlue' if e.type == 'mousedown' else 'SteelBlue'\n    ii.content += f'\u003Ccircle cx=\"{e.image_x}\" cy=\"{e.image_y}\" r=\"15\" fill=\"none\" stroke=\"{color}\" stroke-width=\"4\" /\u003E'\n    ui.notify(f'{e.type} at ({e.image_x:.1f}, {e.image_y:.1f})')\n\nsrc = 'https://picsum.photos/id/565/640/360'\nii = ui.interactive_image(src, on_mouse=mouse_handler, events=['mousedown', 'mouseup'], cross=True)\n\nui.run()",
    "url": "/documentation/interactive_image#interactive_image"
  },
  {
    "title": "ui.interactive_image: Adding layers",
    "content": "In some cases you might want to add different groups of SVG elements to an image.\nMaybe there is one element that needs frequent updates, while the other elements are rarely changed.\nPutting all elements in the same SVG can lead to performance issues,\nbecause the whole SVG needs to be sent to the client whenever one of the elements changes.\n\nThe solution is to add multiple layers to the image.\nEach layer is a separate SVG element, which means that each layer can be updated independently.\n\nThe following demo shows this concept in action, even though both layers are changed at the same time.\n\n*Added in version 2.17.0*",
    "format": "md",
    "demo": "from nicegui import events, ui\n\ndef mouse_handler(e: events.MouseEventArguments):\n    image.content += f'\u003Ccircle cx=\"{e.image_x}\" cy=\"{e.image_y}\" r=\"30\" fill=\"none\" stroke=\"red\" stroke-width=\"4\" /\u003E'\n    highlight.content = f'\u003Ccircle cx=\"{e.image_x}\" cy=\"{e.image_y}\" r=\"28\" fill=\"yellow\" opacity=\"0.5\" /\u003E'\n\nsrc = 'https://picsum.photos/id/674/640/360'\nimage = ui.interactive_image(src, on_mouse=mouse_handler, cross=True)\nhighlight = image.add_layer()\n\nui.run()",
    "url": "/documentation/interactive_image#adding_layers"
  },
  {
    "title": "ui.interactive_image: Nesting elements",
    "content": "You can nest elements inside an interactive image.\nUse Tailwind classes like \"absolute top-0 left-0\" to position the label absolutely with respect to the image.\nOf course this can be done with plain CSS as well.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.interactive_image('https://picsum.photos/id/147/640/360'):\n    ui.button(on_click=lambda: ui.notify('thumbs up'), icon='thumb_up') \\\n        .props('flat fab color=white') \\\n        .classes('absolute bottom-0 left-0 m-2')\n\nui.run()",
    "url": "/documentation/interactive_image#nesting_elements"
  },
  {
    "title": "ui.interactive_image: Force reload",
    "content": "You can force an image to reload by calling the `force_reload` method.\nIt will append a timestamp to the image URL, which will make the browser reload the image.",
    "format": "md",
    "demo": "from nicegui import ui\n\nimg = ui.interactive_image('https://picsum.photos/640/360').classes('w-64')\n\nui.button('Force reload', on_click=img.force_reload)\n\nui.run()",
    "url": "/documentation/interactive_image#force_reload"
  },
  {
    "title": "ui.interactive_image: Blank canvas",
    "content": "You can also create a blank canvas with a given size.\nThis is useful if you want to draw something without loading a background image.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.interactive_image(\n    size=(800, 600), cross=True,\n    on_mouse=lambda e: e.sender.set_content(f'''\n        \u003Ccircle cx=\"{e.image_x}\" cy=\"{e.image_y}\" r=\"50\" fill=\"orange\" /\u003E\n    '''),\n).classes('w-64 bg-blue-50')\n\nui.run()",
    "url": "/documentation/interactive_image#blank_canvas"
  },
  {
    "title": "ui.interactive_image: Loaded event",
    "content": "You can listen to the \"loaded\" event to know when the image has been loaded.",
    "format": "md",
    "demo": "import time\nfrom nicegui import ui\n\nii = ui.interactive_image('https://picsum.photos/640/360')\nii.on('loaded', lambda e: ui.notify(f'loaded {e.args}'))\nui.button('Change Source', on_click=lambda: ii.set_source(f'https://picsum.photos/640/360?time={time.time()}'))\n\nui.run()",
    "url": "/documentation/interactive_image#loaded_event"
  },
  {
    "title": "ui.interactive_image: Crosshairs",
    "content": "You can show crosshairs by passing `cross=True`.\nYou can also change the color of the crosshairs by passing a color string.\n\n*Since version 2.4.0:*\nYou can use the `add_slot` method to add a custom \"cross\" slot with your own SVG template.\nThe `props.x` and `props.y` variables will be available in the template, representing the crosshair position.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.interactive_image('https://picsum.photos/id/565/640/360', cross='red')\n\nui.interactive_image('https://picsum.photos/id/565/640/360').add_slot('cross', '''\n    \u003Ccircle :cx=\"props.x\" :cy=\"props.y\" r=\"30\" stroke=\"red\" fill=\"none\" /\u003E\n    \u003Cline :x1=\"props.x - 30\" :y1=\"props.y\" :x2=\"props.x + 30\" :y2=\"props.y\" stroke=\"red\" /\u003E\n    \u003Cline :x1=\"props.x\" :y1=\"props.y - 30\" :x2=\"props.x\" :y2=\"props.y + 30\" stroke=\"red\" /\u003E\n''')\n\nui.run()",
    "url": "/documentation/interactive_image#crosshairs"
  },
  {
    "title": "ui.interactive_image: SVG events",
    "content": "You can subscribe to events of the SVG elements by using the `on` method with an \"svg:\" prefix.\nMake sure to set `pointer-events=\"all\"` for the SVG elements you want to receive events from.\n\nCurrently the following SVG events are supported:\n\n- pointermove\n- pointerdown\n- pointerup\n- pointerover\n- pointerout\n- pointerenter\n- pointerleave\n- pointercancel",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.interactive_image('https://picsum.photos/id/565/640/360', cross=True, content='''\n    \u003Crect id=\"A\" x=\"85\" y=\"70\" width=\"80\" height=\"60\" fill=\"none\" stroke=\"red\" pointer-events=\"all\" cursor=\"pointer\" /\u003E\n    \u003Crect id=\"B\" x=\"180\" y=\"70\" width=\"80\" height=\"60\" fill=\"none\" stroke=\"red\" pointer-events=\"all\" cursor=\"pointer\" /\u003E\n''').on('svg:pointerdown', lambda e: ui.notify(f'SVG clicked: {e.args}'))\n\nui.run()",
    "url": "/documentation/interactive_image#svg_events"
  },
  {
    "title": "ui.interactive_image: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/interactive_image#reference"
  },
  {
    "title": "ui.video: Video",
    "content": "Displays a video.\n\n:param src: URL or local file path of the video source\n:param controls: whether to show the video controls, like play, pause, and volume (default: `True`)\n:param autoplay: whether to start playing the video automatically (default: `False`)\n:param muted: whether the video should be initially muted (default: `False`)\n:param loop: whether the video should loop (default: `False`)\n\nSee `here \u003Chttps://developer.mozilla.org/en-US/docs/Web/HTML/Element/video#events\u003E`_\nfor a list of events you can subscribe to using the generic event subscription `on()`.\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nv = ui.video('https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/360/Big_Buck_Bunny_360_10s_1MB.mp4')\nv.on('ended', lambda _: ui.notify('Video playback completed'))\n\nui.run()",
    "url": "/documentation/video#video"
  },
  {
    "title": "ui.video: Control the video element",
    "content": "This demo shows how to play, pause and seek programmatically.",
    "format": "md",
    "demo": "from nicegui import ui\n\nv = ui.video('https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/360/Big_Buck_Bunny_360_10s_1MB.mp4')\nui.button('Play', on_click=v.play)\nui.button('Pause', on_click=v.pause)\nui.button('Jump to 0:05', on_click=lambda: v.seek(5))\n\nui.run()",
    "url": "/documentation/video#control_the_video_element"
  },
  {
    "title": "ui.video: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/video#reference"
  },
  {
    "title": "Audiovisual Elements: Image",
    "content": "Displays an image.\nThis element is based on Quasar's `QImg \u003Chttps://quasar.dev/vue-components/img\u003E`_ component.\n\n:param source: the source of the image; can be a URL, local file path, a base64 string or a PIL image\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.image('https://picsum.photos/id/377/640/360')\n\nui.run()",
    "url": "/documentation/section_audiovisual_elements#image"
  },
  {
    "title": "Audiovisual Elements: Captions and Overlays",
    "content": "By nesting elements inside a `ui.image` you can create augmentations.\n\nUse [Quasar classes](https://quasar.dev/vue-components/img) for positioning and styling captions.\nTo overlay an SVG, make the `viewBox` exactly the size of the image and provide `100%` width/height to match the actual rendered size.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.image('https://picsum.photos/id/29/640/360'):\n    ui.label('Nice!').classes('absolute-bottom text-subtitle2 text-center')\n\nwith ui.image('https://cdn.stocksnap.io/img-thumbs/960w/airplane-sky_DYPWDEEILG.jpg'):\n    ui.html('''\n        \u003Csvg viewBox=\"0 0 960 638\" width=\"100%\" height=\"100%\" xmlns=\"http://www.w3.org/2000/svg\"\u003E\n        \u003Ccircle cx=\"445\" cy=\"300\" r=\"100\" fill=\"none\" stroke=\"red\" stroke-width=\"10\" /\u003E\n        \u003C/svg\u003E\n    ''').classes('w-full bg-transparent')\n\nui.run()",
    "url": "/documentation/section_audiovisual_elements#captions_and_overlays"
  },
  {
    "title": "Audiovisual Elements: Interactive Image",
    "content": "Create an image with an SVG overlay that handles mouse events and yields image coordinates.\nIt is also the best choice for non-flickering image updates.\nIf the source URL changes faster than images can be loaded by the browser, some images are simply skipped.\nThereby repeatedly updating the image source will automatically adapt to the available bandwidth.\nSee `OpenCV Webcam \u003Chttps://github.com/zauberzeug/nicegui/tree/main/examples/opencv_webcam/main.py\u003E`_ for an example.\n\nThe mouse event handler is called with mouse event arguments containing\n\n- `type` (the name of the JavaScript event),\n- `image_x` and `image_y` (image coordinates in pixels),\n- `button` and `buttons` (mouse button numbers from the JavaScript event), as well as\n- `alt`, `ctrl`, `meta`, and `shift` (modifier keys from the JavaScript event).\n\nYou can also pass a tuple of width and height instead of an image source.\nThis will create an empty image with the given size.\n\n:param source: the source of the image; can be an URL, local file path, a base64 string or just an image size\n:param content: SVG content which should be overlaid; viewport has the same dimensions as the image\n:param size: size of the image (width, height) in pixels; only used if `source` is not set\n:param on_mouse: callback for mouse events (contains image coordinates `image_x` and `image_y` in pixels)\n:param events: list of JavaScript events to subscribe to (default: `['click']`)\n:param cross: whether to show crosshairs or a color string (default: `False`)\n",
    "format": "rst",
    "demo": "from nicegui import events, ui\n\ndef mouse_handler(e: events.MouseEventArguments):\n    color = 'SkyBlue' if e.type == 'mousedown' else 'SteelBlue'\n    ii.content += f'\u003Ccircle cx=\"{e.image_x}\" cy=\"{e.image_y}\" r=\"15\" fill=\"none\" stroke=\"{color}\" stroke-width=\"4\" /\u003E'\n    ui.notify(f'{e.type} at ({e.image_x:.1f}, {e.image_y:.1f})')\n\nsrc = 'https://picsum.photos/id/565/640/360'\nii = ui.interactive_image(src, on_mouse=mouse_handler, events=['mousedown', 'mouseup'], cross=True)\n\nui.run()",
    "url": "/documentation/section_audiovisual_elements#interactive_image"
  },
  {
    "title": "Audiovisual Elements: Audio",
    "content": "Displays an audio player.\n\n:param src: URL or local file path of the audio source\n:param controls: whether to show the audio controls, like play, pause, and volume (default: `True`)\n:param autoplay: whether to start playing the audio automatically (default: `False`)\n:param muted: whether the audio should be initially muted (default: `False`)\n:param loop: whether the audio should loop (default: `False`)\n\nSee `here \u003Chttps://developer.mozilla.org/en-US/docs/Web/HTML/Element/audio#events\u003E`_\nfor a list of events you can subscribe to using the generic event subscription `on()`.\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\na = ui.audio('https://cdn.pixabay.com/download/audio/2022/02/22/audio_d1718ab41b.mp3')\na.on('ended', lambda _: ui.notify('Audio playback completed'))\n\nui.button(on_click=lambda: a.props('muted'), icon='volume_off').props('outline')\nui.button(on_click=lambda: a.props(remove='muted'), icon='volume_up').props('outline')\n\nui.run()",
    "url": "/documentation/section_audiovisual_elements#audio"
  },
  {
    "title": "Audiovisual Elements: Video",
    "content": "Displays a video.\n\n:param src: URL or local file path of the video source\n:param controls: whether to show the video controls, like play, pause, and volume (default: `True`)\n:param autoplay: whether to start playing the video automatically (default: `False`)\n:param muted: whether the video should be initially muted (default: `False`)\n:param loop: whether the video should loop (default: `False`)\n\nSee `here \u003Chttps://developer.mozilla.org/en-US/docs/Web/HTML/Element/video#events\u003E`_\nfor a list of events you can subscribe to using the generic event subscription `on()`.\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nv = ui.video('https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/360/Big_Buck_Bunny_360_10s_1MB.mp4')\nv.on('ended', lambda _: ui.notify('Video playback completed'))\n\nui.run()",
    "url": "/documentation/section_audiovisual_elements#video"
  },
  {
    "title": "Audiovisual Elements: Icon",
    "content": "This element is based on Quasar's `QIcon \u003Chttps://quasar.dev/vue-components/icon\u003E`_ component.\n\n`Here \u003Chttps://fonts.google.com/icons?icon.set=Material+Icons\u003E`_ is a reference of possible names.\n\n:param name: name of the icon (snake case, e.g. `add_circle`)\n:param size: size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl), examples: 16px, 2rem\n:param color: icon color (either a Quasar, Tailwind, or CSS color or `None`, default: `None`)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.icon('thumb_up', color='primary').classes('text-5xl')\n\nui.run()",
    "url": "/documentation/section_audiovisual_elements#icon"
  },
  {
    "title": "Audiovisual Elements: Avatar",
    "content": "A avatar element wrapping Quasar's\n`QAvatar \u003Chttps://quasar.dev/vue-components/avatar\u003E`_ component.\n\n:param icon: name of the icon or image path with \"img:\" prefix (e.g. \"map\", \"img:path/to/image.png\")\n:param color: background color (either a Quasar, Tailwind, or CSS color or `None`, default: \"primary\")\n:param text_color: color name from the Quasar Color Palette (e.g. \"primary\", \"teal-10\")\n:param size: size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl) (e.g. \"16px\", \"2rem\")\n:param font_size: size in CSS units, including unit name, of the content (icon, text) (e.g. \"18px\", \"2rem\")\n:param square: removes border-radius so borders are squared (default: False)\n:param rounded: applies a small standard border-radius for a squared shape of the component (default: False)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.avatar('favorite_border', text_color='grey-11', square=True)\nui.avatar('img:https://nicegui.io/logo_square.png', color='blue-2')\n\nui.run()",
    "url": "/documentation/section_audiovisual_elements#avatar"
  },
  {
    "title": "Audiovisual Elements: SVG",
    "content": "You can add Scalable Vector Graphics using the `ui.html` element.",
    "format": "md",
    "demo": "from nicegui import ui\n\ncontent = '''\n    \u003Csvg viewBox=\"0 0 200 200\" width=\"100\" height=\"100\" xmlns=\"http://www.w3.org/2000/svg\"\u003E\n    \u003Ccircle cx=\"100\" cy=\"100\" r=\"78\" fill=\"#ffde34\" stroke=\"black\" stroke-width=\"3\" /\u003E\n    \u003Ccircle cx=\"80\" cy=\"85\" r=\"8\" /\u003E\n    \u003Ccircle cx=\"120\" cy=\"85\" r=\"8\" /\u003E\n    \u003Cpath d=\"m60,120 C75,150 125,150 140,120\" style=\"fill:none; stroke:black; stroke-width:8; stroke-linecap:round\" /\u003E\n    \u003C/svg\u003E'''\nui.html(content)\n\nui.run()",
    "url": "/documentation/section_audiovisual_elements#svg"
  },
  {
    "title": "Binding Properties: Bindings",
    "content": "NiceGUI is able to directly bind UI elements to models.\nBinding is possible for UI element properties like text, value or visibility and for model properties that are (nested) class attributes.\nEach element provides methods like `bind_value` and `bind_visibility` to create a two-way binding with the corresponding property.\nTo define a one-way binding use the `_from` and `_to` variants of these methods.\nJust pass a property of the model as parameter to these methods to create the binding.\nThe values will be updated immediately and whenever one of them changes.",
    "format": "md",
    "demo": "from nicegui import ui\n\nclass Demo:\n    def __init__(self):\n        self.number = 1\n\ndemo = Demo()\nv = ui.checkbox('visible', value=True)\nwith ui.column().bind_visibility_from(v, 'value'):\n    ui.slider(min=1, max=3).bind_value(demo, 'number')\n    ui.toggle({1: 'A', 2: 'B', 3: 'C'}).bind_value(demo, 'number')\n    ui.number().bind_value(demo, 'number')\n\nui.run()",
    "url": "/documentation/section_binding_properties#bindings"
  },
  {
    "title": "Binding Properties: Transformation functions",
    "content": "You can use ``forward`` and ``backward`` transformation functions to convert the value\nwhen propagating it from one object to another.\nThese functions are called whenever the source attribute changes,\nor - in case of active links (see below) - whenever the source attribute is checked for changes.\n\nNote:\nNiceGUI 2.16.0 improved efficiency of binding propagation by strictly adhering to a Depth-First-Search approach,\nupdating every affected node once and executing the transformation function once.\nIf you are migrating from NiceGUI 2.15.0 or older, there may be extra runs on transformation functions,\nespecially ones in the opposite direction to the current propagation direction,\nwhich are no-longer ran in NiceGUI 2.16.0.\nAs a result, you would need to change your code appropriately.\n\nWe would also like to mention that, for the most stable behaviour across releases,\nit is best-practice that transform functions have no side-effects and do basic transform operations only.\nThis way, it will not matter how NiceGUI chooses to call them in what order and by how many times.",
    "format": "md",
    "demo": "from nicegui import ui\n\ni = ui.input(value='Lorem ipsum')\nui.label().bind_text_from(i, 'value',\n                          backward=lambda text: f'{len(text)} characters')\n\nui.run()",
    "url": "/documentation/section_binding_properties#transformation_functions"
  },
  {
    "title": "Binding Properties: Bind to dictionary",
    "content": "Here we are binding the text of labels to a dictionary.",
    "format": "md",
    "demo": "from nicegui import ui\n\ndata = {'name': 'Bob', 'age': 17}\n\nui.label().bind_text_from(data, 'name', backward=lambda n: f'Name: {n}')\nui.label().bind_text_from(data, 'age', backward=lambda a: f'Age: {a}')\n\nui.button('Turn 18', on_click=lambda: data.update(age=18))\n\nui.run()",
    "url": "/documentation/section_binding_properties#bind_to_dictionary"
  },
  {
    "title": "Binding Properties: Bind to variable",
    "content": "Here we are binding the value from the datepicker to a bare variable.\nTherefore we use the dictionary `globals()` which contains all global variables.\nThis demo is based on the [official datepicker example](/documentation/date#input_element_with_date_picker).",
    "format": "md",
    "demo": "from nicegui import ui\n\ndate = '2023-01-01'\n\nwith ui.input('Date').bind_value(globals(), 'date') as date_input:\n    with ui.menu() as menu:\n        ui.date(on_change=lambda: ui.notify(f'Date: {date}')).bind_value(date_input)\n    with date_input.add_slot('append'):\n        ui.icon('edit_calendar').on('click', menu.open).classes('cursor-pointer')\n\nui.run()",
    "url": "/documentation/section_binding_properties#bind_to_variable"
  },
  {
    "title": "Binding Properties: Bind to storage",
    "content": "Bindings also work with [`app.storage`](/documentation/storage).\nHere we are storing the value of a textarea between visits.\nThe note is also shared between all tabs of the same user.",
    "format": "md",
    "demo": "from nicegui import app, ui\n\n@ui.page('/')\ndef index():\n    ui.textarea('This note is kept between visits')\n        .classes('w-full').bind_value(app.storage.user, 'note')\n\nui.run()",
    "url": "/documentation/section_binding_properties#bind_to_storage"
  },
  {
    "title": "Binding Properties: Bindable properties for maximum performance",
    "content": "There are two types of bindings:\n\n1. \"Bindable properties\" automatically detect write access and trigger the value propagation.\n    Most NiceGUI elements use these bindable properties, like `value` in `ui.input` or `text` in `ui.label`.\n    Basically all properties with `bind()` methods support this type of binding.\n2. All other bindings are sometimes called \"active links\".\n    If you bind a label text to some dictionary entry or an attribute of a custom data model,\n    NiceGUI's binding module has to actively check if the value changed.\n    This is done in a `refresh_loop()` which runs every 0.1 seconds.\n    The interval can be configured via `binding_refresh_interval` in `ui.run()`.\n\nThe \"bindable properties\" are very efficient and don't cost anything as long as the values don't change.\nBut the \"active links\" need to check all bound values 10 times per second.\nThis can get costly, especially if you bind to complex objects like lists or dictionaries.\n\nBecause it is crucial not to block the main thread for too long,\nwe show a warning if one step of the `refresh_loop()` takes too long.\nYou can configure the threshold via `binding.MAX_PROPAGATION_TIME` which defaults to 0.01 seconds.\nBut often the warning is a valuable indicator for a performance or memory issue.\nIf your CPU would be busy updating bindings a significant duration,\nnothing else could happen on the main thread and the UI \"hangs\".\n\nThe following demo shows how to define and use bindable properties for a `Demo` class like in the first demo.\nThe `number` property is now a `BindableProperty`,\nwhich allows NiceGUI to detect write access and trigger the value propagation immediately.",
    "format": "md",
    "demo": "from nicegui import binding, ui\n\nclass Demo:\n    number = binding.BindableProperty()\n\n    def __init__(self):\n        self.number = 1\n\ndemo = Demo()\nui.slider(min=1, max=3).bind_value(demo, 'number')\nui.toggle({1: 'A', 2: 'B', 3: 'C'}).bind_value(demo, 'number')\nui.number(min=1, max=3).bind_value(demo, 'number')\n\nui.run()",
    "url": "/documentation/section_binding_properties#bindable_properties_for_maximum_performance"
  },
  {
    "title": "Binding Properties: Bindable dataclass",
    "content": "The `bindable_dataclass` decorator provides a convenient way to create classes with bindable properties.\nIt extends the functionality of Python's standard `dataclasses.dataclass` decorator\nby automatically making all dataclass fields bindable.\nThis eliminates the need to manually declare each field as a `BindableProperty`\nwhile retaining all the benefits of regular dataclasses.\n\n*Added in version 2.11.0*",
    "format": "md",
    "demo": "from nicegui import binding, ui\n\n@binding.bindable_dataclass\nclass Demo:\n    number: int = 1\n\ndemo = Demo()\nui.slider(min=1, max=3).bind_value(demo, 'number')\nui.toggle({1: 'A', 2: 'B', 3: 'C'}).bind_value(demo, 'number')\nui.number(min=1, max=3).bind_value(demo, 'number')\n\nui.run()",
    "url": "/documentation/section_binding_properties#bindable_dataclass"
  },
  {
    "title": "ui.run: ui.run",
    "content": "You can call `ui.run()` with optional arguments.\nMost of them only apply after stopping and fully restarting the app and do not apply with auto-reloading.\n\n:param host: start server with this host (defaults to `'127.0.0.1` in native mode, otherwise `'0.0.0.0'`)\n:param port: use this port (default: 8080 in normal mode, and an automatically determined open port in native mode)\n:param title: page title (default: `'NiceGUI'`, can be overwritten per page)\n:param viewport: page meta viewport content (default: `'width=device-width, initial-scale=1'`, can be overwritten per page)\n:param favicon: relative filepath, absolute URL to a favicon (default: `None`, NiceGUI icon will be used) or emoji (e.g. `'🚀'`, works for most browsers)\n:param dark: whether to use Quasar's dark mode (default: `False`, use `None` for \"auto\" mode)\n:param language: language for Quasar elements (default: `'en-US'`)\n:param binding_refresh_interval: time between binding updates (default: `0.1` seconds, bigger is more CPU friendly)\n:param reconnect_timeout: maximum time the server waits for the browser to reconnect (default: 3.0 seconds)\n:param message_history_length: maximum number of messages that will be stored and resent after a connection interruption (default: 1000, use 0 to disable, *added in version 2.9.0*)\n:param cache_control_directives: cache control directives for internal static files (default: `'public, max-age=31536000, immutable, stale-while-revalidate=31536000'`)\n:param fastapi_docs: enable FastAPI's automatic documentation with Swagger UI, ReDoc, and OpenAPI JSON (bool or dictionary as described `here \u003Chttps://fastapi.tiangolo.com/tutorial/metadata/\u003E`_, default: `False`, *updated in version 2.9.0*)\n:param show: automatically open the UI in a browser tab (default: `True`)\n:param on_air: tech preview: `allows temporary remote access \u003Chttps://nicegui.io/documentation/section_configuration_deployment#nicegui_on_air\u003E`_ if set to `True` (default: disabled)\n:param native: open the UI in a native window of size 800x600 (default: `False`, deactivates `show`, automatically finds an open port)\n:param window_size: open the UI in a native window with the provided size (e.g. `(1024, 786)`, default: `None`, also activates `native`)\n:param fullscreen: open the UI in a fullscreen window (default: `False`, also activates `native`)\n:param frameless: open the UI in a frameless window (default: `False`, also activates `native`)\n:param reload: automatically reload the UI on file changes (default: `True`)\n:param uvicorn_logging_level: logging level for uvicorn server (default: `'warning'`)\n:param uvicorn_reload_dirs: string with comma-separated list for directories to be monitored (default is current working directory only)\n:param uvicorn_reload_includes: string with comma-separated list of glob-patterns which trigger reload on modification (default: `'*.py'`)\n:param uvicorn_reload_excludes: string with comma-separated list of glob-patterns which should be ignored for reload (default: `'.*, .py[cod], .sw.*, ~*'`)\n:param tailwind: whether to use Tailwind (experimental, default: `True`)\n:param prod_js: whether to use the production version of Vue and Quasar dependencies (default: `True`)\n:param endpoint_documentation: control what endpoints appear in the autogenerated OpenAPI docs (default: 'none', options: 'none', 'internal', 'page', 'all')\n:param storage_secret: secret key for browser-based storage (default: `None`, a value is required to enable ui.storage.individual and ui.storage.browser)\n:param show_welcome_message: whether to show the welcome message (default: `True`)\n:param kwargs: additional keyword arguments are passed to `uvicorn.run`\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.label('page with custom title')\n\nui.run(title='My App')",
    "url": "/documentation/run#ui_run"
  },
  {
    "title": "ui.run: Emoji favicon",
    "content": "You can use an emoji as favicon.\nThis works in Chrome, Firefox and Safari.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.label('NiceGUI rocks!')\n\nui.run(favicon='🚀')",
    "url": "/documentation/run#emoji_favicon"
  },
  {
    "title": "ui.run: Base64 favicon",
    "content": "You can also use an base64-encoded image as favicon.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.label('NiceGUI with a red dot!')\n\nicon = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=='\n\nui.run(favicon=icon)",
    "url": "/documentation/run#base64_favicon"
  },
  {
    "title": "ui.run: SVG favicon",
    "content": "And directly use an SVG as favicon.\nWorks in Chrome, Firefox and Safari.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.label('NiceGUI makes you smile!')\n\nsmiley = '''\n    \u003Csvg viewBox=\"0 0 200 200\" xmlns=\"http://www.w3.org/2000/svg\"\u003E\n        \u003Ccircle cx=\"100\" cy=\"100\" r=\"78\" fill=\"#ffde34\" stroke=\"black\" stroke-width=\"3\" /\u003E\n        \u003Ccircle cx=\"80\" cy=\"85\" r=\"8\" /\u003E\n        \u003Ccircle cx=\"120\" cy=\"85\" r=\"8\" /\u003E\n        \u003Cpath d=\"m60,120 C75,150 125,150 140,120\" style=\"fill:none; stroke:black; stroke-width:8; stroke-linecap:round\" /\u003E\n    \u003C/svg\u003E\n'''\n\nui.run(favicon=smiley)",
    "url": "/documentation/run#svg_favicon"
  },
  {
    "title": "ui.run: Custom welcome message",
    "content": "You can mute the default welcome message on the command line setting the `show_welcome_message` to `False`.\nInstead you can print your own welcome message with a custom startup handler.",
    "format": "md",
    "demo": "from nicegui import app, ui\n\nui.label('App with custom welcome message')\n\napp.on_startup(lambda: print('Visit your app on one of these URLs:', app.urls))\n\nui.run(show_welcome_message=False)",
    "url": "/documentation/run#custom_welcome_message"
  },
  {
    "title": "Configuration & Deployment: URLs",
    "content": "You can access the list of all URLs on which the NiceGUI app is available via `app.urls`.\nThe URLs are not available in `app.on_startup` because the server is not yet running.\nInstead, you can access them in a page function or register a callback with `app.urls.on_change`.",
    "format": "md",
    "demo": "from nicegui import app, ui\n\n@ui.page('/')\ndef index():\n    for url in app.urls:\n        ui.link(url, target=url)\n\nui.run()",
    "url": "/documentation/section_configuration_deployment#urls"
  },
  {
    "title": "Configuration & Deployment: ui.run",
    "content": "You can call `ui.run()` with optional arguments.\nMost of them only apply after stopping and fully restarting the app and do not apply with auto-reloading.\n\n:param host: start server with this host (defaults to `'127.0.0.1` in native mode, otherwise `'0.0.0.0'`)\n:param port: use this port (default: 8080 in normal mode, and an automatically determined open port in native mode)\n:param title: page title (default: `'NiceGUI'`, can be overwritten per page)\n:param viewport: page meta viewport content (default: `'width=device-width, initial-scale=1'`, can be overwritten per page)\n:param favicon: relative filepath, absolute URL to a favicon (default: `None`, NiceGUI icon will be used) or emoji (e.g. `'🚀'`, works for most browsers)\n:param dark: whether to use Quasar's dark mode (default: `False`, use `None` for \"auto\" mode)\n:param language: language for Quasar elements (default: `'en-US'`)\n:param binding_refresh_interval: time between binding updates (default: `0.1` seconds, bigger is more CPU friendly)\n:param reconnect_timeout: maximum time the server waits for the browser to reconnect (default: 3.0 seconds)\n:param message_history_length: maximum number of messages that will be stored and resent after a connection interruption (default: 1000, use 0 to disable, *added in version 2.9.0*)\n:param cache_control_directives: cache control directives for internal static files (default: `'public, max-age=31536000, immutable, stale-while-revalidate=31536000'`)\n:param fastapi_docs: enable FastAPI's automatic documentation with Swagger UI, ReDoc, and OpenAPI JSON (bool or dictionary as described `here \u003Chttps://fastapi.tiangolo.com/tutorial/metadata/\u003E`_, default: `False`, *updated in version 2.9.0*)\n:param show: automatically open the UI in a browser tab (default: `True`)\n:param on_air: tech preview: `allows temporary remote access \u003Chttps://nicegui.io/documentation/section_configuration_deployment#nicegui_on_air\u003E`_ if set to `True` (default: disabled)\n:param native: open the UI in a native window of size 800x600 (default: `False`, deactivates `show`, automatically finds an open port)\n:param window_size: open the UI in a native window with the provided size (e.g. `(1024, 786)`, default: `None`, also activates `native`)\n:param fullscreen: open the UI in a fullscreen window (default: `False`, also activates `native`)\n:param frameless: open the UI in a frameless window (default: `False`, also activates `native`)\n:param reload: automatically reload the UI on file changes (default: `True`)\n:param uvicorn_logging_level: logging level for uvicorn server (default: `'warning'`)\n:param uvicorn_reload_dirs: string with comma-separated list for directories to be monitored (default is current working directory only)\n:param uvicorn_reload_includes: string with comma-separated list of glob-patterns which trigger reload on modification (default: `'*.py'`)\n:param uvicorn_reload_excludes: string with comma-separated list of glob-patterns which should be ignored for reload (default: `'.*, .py[cod], .sw.*, ~*'`)\n:param tailwind: whether to use Tailwind (experimental, default: `True`)\n:param prod_js: whether to use the production version of Vue and Quasar dependencies (default: `True`)\n:param endpoint_documentation: control what endpoints appear in the autogenerated OpenAPI docs (default: 'none', options: 'none', 'internal', 'page', 'all')\n:param storage_secret: secret key for browser-based storage (default: `None`, a value is required to enable ui.storage.individual and ui.storage.browser)\n:param show_welcome_message: whether to show the welcome message (default: `True`)\n:param kwargs: additional keyword arguments are passed to `uvicorn.run`\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.label('page with custom title')\n\nui.run(title='My App')",
    "url": "/documentation/section_configuration_deployment#ui_run"
  },
  {
    "title": "Configuration & Deployment: Native Mode",
    "content": "You can enable native mode for NiceGUI by specifying `native=True` in the `ui.run` function.\nTo customize the initial window size and display mode, use the `window_size` and `fullscreen` parameters respectively.\nAdditionally, you can provide extra keyword arguments via `app.native.window_args` and `app.native.start_args`.\nPick any parameter as it is defined by the internally used [pywebview module](https://pywebview.flowrl.com/api)\nfor the `webview.create_window` and `webview.start` functions.\nNote that these keyword arguments will take precedence over the parameters defined in `ui.run`.\n\nAdditionally, you can change `webview.settings` via `app.native.settings`.\n\nIn native mode the `app.native.main_window` object allows you to access the underlying window.\nIt is an async version of [`Window` from pywebview](https://pywebview.flowrl.com/api/#webview-window).",
    "format": "md",
    "demo": "from nicegui import app, ui\n\napp.native.window_args['resizable'] = False\napp.native.start_args['debug'] = True\napp.native.settings['ALLOW_DOWNLOADS'] = True\n\nui.label('app running in native mode')\nui.button('enlarge', on_click=lambda: app.native.main_window.resize(1000, 700))\n\nui.run(native=True, window_size=(400, 300), fullscreen=False)",
    "url": "/documentation/section_configuration_deployment#native_mode"
  },
  {
    "title": "Configuration & Deployment: ",
    "content": "\n    Note that the native app is run in a separate\n    [process](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Process).\n    Therefore any configuration changes from code run under a\n    [main guard](https://docs.python.org/3/library/__main__.html#idiomatic-usage) is ignored by the native app.\n    The following examples show the difference between a working and a non-working configuration.\n",
    "format": "md",
    "demo": "",
    "url": "/documentation/section_configuration_deployment#None"
  },
  {
    "title": "Configuration & Deployment: None",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/section_configuration_deployment#None"
  },
  {
    "title": "Configuration & Deployment: ",
    "content": "\n    If webview has trouble finding required libraries, you may get an error relating to \"WebView2Loader.dll\".\n    To work around this issue, try moving the DLL file up a directory, e.g.:\n\n    * from `.venv/Lib/site-packages/webview/lib/x64/WebView2Loader.dll`\n    * to `.venv/Lib/site-packages/webview/lib/WebView2Loader.dll`\n",
    "format": "md",
    "demo": "",
    "url": "/documentation/section_configuration_deployment#None"
  },
  {
    "title": "Configuration & Deployment: Environment Variables",
    "content": "You can set the following environment variables to configure NiceGUI:\n\n- `MATPLOTLIB` (default: true) can be set to `false` to avoid the potentially costly import of Matplotlib.\n    This will make `ui.pyplot` and `ui.line_plot` unavailable.\n- `NICEGUI_STORAGE_PATH` (default: local \".nicegui\") can be set to change the location of the storage files.\n- `MARKDOWN_CONTENT_CACHE_SIZE` (default: 1000): The maximum number of Markdown content snippets that are cached in memory.\n- `RST_CONTENT_CACHE_SIZE` (default: 1000): The maximum number of ReStructuredText content snippets that are cached in memory.\n- `NICEGUI_REDIS_URL` (default: None, means local file storage): The URL of the Redis server to use for shared persistent storage.\n- `NICEGUI_REDIS_KEY_PREFIX` (default: \"nicegui:\"): The prefix for Redis keys.",
    "format": "md",
    "demo": "from nicegui import ui\nfrom nicegui.elements import markdown\n\nui.label(f'Markdown content cache size is {markdown.prepare_content.cache_info().maxsize}')\n\nui.run()",
    "url": "/documentation/section_configuration_deployment#environment_variables"
  },
  {
    "title": "Configuration & Deployment: Background Tasks",
    "content": "`background_tasks.create()` allows you to run an async function in the background and return a task object.\nBy default the task will be automatically cancelled during shutdown.\nYou can prevent this by using the `@background_tasks.await_on_shutdown` decorator (added in version 2.16.0).\nThis is useful for tasks that need to be completed even when the app is shutting down.",
    "format": "md",
    "demo": "import aiofiles\nimport asyncio\nfrom nicegui import background_tasks, ui\n\nresults = {'answer': '?'}\n\nasync def compute() -\u003E None:\n    await asyncio.sleep(1)\n    results['answer'] = 42\n\n@background_tasks.await_on_shutdown\nasync def backup() -\u003E None:\n    await asyncio.sleep(1)\n    async with aiofiles.open('backup.json', 'w') as f:\n        await f.write(f'{results[\"answer\"]}')\n    print('backup.json written', flush=True)\n\nui.label().bind_text_from(results, 'answer', lambda x: f'answer: {x}')\nui.button('Compute', on_click=lambda: background_tasks.create(compute()))\nui.button('Backup', on_click=lambda: background_tasks.create(backup()))\n\nui.run()",
    "url": "/documentation/section_configuration_deployment#background_tasks"
  },
  {
    "title": "Configuration & Deployment: Custom Vue Components",
    "content": "\n    You can create custom components by subclassing `ui.element` and implementing a corresponding Vue component.\n    The [\"Custom Vue components\" example](https://github.com/zauberzeug/nicegui/tree/main/examples/custom_vue_component)\n    demonstrates how to create a custom counter component which emits events and receives updates from the server.\n\n    The [\"Signature pad\" example](https://github.com/zauberzeug/nicegui/blob/main/examples/signature_pad)\n    shows how to define dependencies for a custom component using a `package.json` file.\n    This allows you to use third-party libraries via NPM in your component.\n\n    Last but not least, the [\"Node module integration\" example](https://github.com/zauberzeug/nicegui/blob/main/examples/node_module_integration)\n    demonstrates how to create a package.json file and a webpack.config.js file to bundle a custom Vue component with its dependencies.\n",
    "format": "md",
    "demo": "",
    "url": "/documentation/section_configuration_deployment#custom_vue_components"
  },
  {
    "title": "Configuration & Deployment: Server Hosting",
    "content": "\n    To deploy your NiceGUI app on a server, you will need to execute your `main.py` (or whichever file contains your `ui.run(...)`) on your cloud infrastructure.\n    You can, for example, just install the [NiceGUI python package via pip](https://pypi.org/project/nicegui/) and use systemd or similar service to start the main script.\n    In most cases, you will set the port to 80 (or 443 if you want to use HTTPS) with the `ui.run` command to make it easily accessible from the outside.\n\n    A convenient alternative is the use of our [pre-built multi-arch Docker image](https://hub.docker.com/r/zauberzeug/nicegui) which contains all necessary dependencies.\n    With this command you can launch the script `main.py` in the current directory on the public port 80:\n",
    "format": "md",
    "demo": "",
    "url": "/documentation/section_configuration_deployment#server_hosting"
  },
  {
    "title": "Configuration & Deployment: None",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/section_configuration_deployment#None"
  },
  {
    "title": "Configuration & Deployment: ",
    "content": "\n    The demo assumes `main.py` uses the port 8080 in the `ui.run` command (which is the default).\n    The `-d` tells docker to run in background and `--restart always` makes sure the container is restarted if the app crashes or the server reboots.\n    Of course this can also be written in a Docker compose file:\n",
    "format": "md",
    "demo": "",
    "url": "/documentation/section_configuration_deployment#None"
  },
  {
    "title": "Configuration & Deployment: None",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/section_configuration_deployment#None"
  },
  {
    "title": "Configuration & Deployment: ",
    "content": "\n    There are other handy features in the Docker image like non-root user execution and signal pass-through.\n    For more details we recommend to have a look at our [Docker example](https://github.com/zauberzeug/nicegui/tree/main/examples/docker_image).\n\n    To serve your application with [HTTPS](https://fastapi.tiangolo.com/deployment/https/) encryption, you can provide SSL certificates in multiple ways.\n    For instance, you can directly provide your certificates to [Uvicorn](https://www.uvicorn.org/), which NiceGUI is based on, by passing the\n    relevant [options](https://www.uvicorn.org/#command-line-options) to `ui.run()`.\n    If both a certificate and key file are provided, the application will automatically be served over HTTPS:\n",
    "format": "md",
    "demo": "",
    "url": "/documentation/section_configuration_deployment#None"
  },
  {
    "title": "Configuration & Deployment: None",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/section_configuration_deployment#None"
  },
  {
    "title": "Configuration & Deployment: ",
    "content": "\n    In production we also like using reverse proxies like [Traefik](https://doc.traefik.io/traefik/) or [NGINX](https://www.nginx.com/) to handle these details for us.\n    See our development [docker-compose.yml](https://github.com/zauberzeug/nicegui/blob/main/docker-compose.yml) as an example based on traefik or\n    [this example nginx.conf file](https://github.com/zauberzeug/nicegui/blob/main/examples/nginx_https/nginx.conf) showing how NGINX can be used to handle the SSL certificates and\n    reverse proxy to your NiceGUI app.\n\n    You may also have a look at [our demo for using a custom FastAPI app](https://github.com/zauberzeug/nicegui/tree/main/examples/fastapi).\n    This will allow you to do very flexible deployments as described in the [FastAPI documentation](https://fastapi.tiangolo.com/deployment/).\n    Note that there are additional steps required to allow multiple workers.\n",
    "format": "md",
    "demo": "",
    "url": "/documentation/section_configuration_deployment#None"
  },
  {
    "title": "Configuration & Deployment: Package for Installation",
    "content": "\n    NiceGUI apps can also be bundled into an executable with `nicegui-pack` which is based on [PyInstaller](https://www.pyinstaller.org/).\n    This allows you to distribute your app as a single file that can be executed on any computer.\n\n    Just make sure to call `ui.run` with `reload=False` in your main script to disable the auto-reload feature.\n    Running the `nicegui-pack` command below will create an executable `myapp` in the `dist` folder:\n",
    "format": "md",
    "demo": "",
    "url": "/documentation/section_configuration_deployment#package_for_installation"
  },
  {
    "title": "Configuration & Deployment: None",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/section_configuration_deployment#None"
  },
  {
    "title": "Configuration & Deployment: ",
    "content": "\n    **Packaging Tips:**\n\n    - When building a PyInstaller app, your main script can use a native window (rather than a browser window) by\n    using `ui.run(reload=False, native=True)`.\n    The `native` parameter can be `True` or `False` depending on whether you want a native window or to launch a\n    page in the user's browser - either will work in the PyInstaller generated app.\n\n    - Specifying `--windowed` to `nicegui-pack` will prevent a terminal console from appearing.\n    However you should only use this option if you have also specified `native=True` in your `ui.run` command.\n    Without a terminal console the user won't be able to exit the app by pressing Ctrl-C.\n    With the `native=True` option, the app will automatically close when the window is closed, as expected.\n\n    - Specifying `--windowed` to `nicegui-pack` will create an `.app` file on Mac which may be more convenient to distribute.\n    When you double-click the app to run it, it will not show any console output.\n    You can also run the app from the command line with `./myapp.app/Contents/MacOS/myapp` to see the console output.\n\n    - Specifying `--onefile` to `nicegui-pack` will create a single executable file.\n    Whilst convenient for distribution, it will be slower to start up.\n    This is not NiceGUI's fault but just the way Pyinstaller zips things into a single file, then unzips everything\n    into a temporary directory before running.\n    You can mitigate this by removing `--onefile` from the `nicegui-pack` command,\n    and zip up the generated `dist` directory yourself, distribute it,\n    and your end users can unzip once and be good to go,\n    without the constant expansion of files due to the `--onefile` flag.\n\n    - Summary of user experience for different options:\n\n        | `nicegui-pack`           | `ui.run(...)`  | Explanation |\n        | :---                     | :---           | :---        |\n        | `onefile`                | `native=False` | Single executable generated in `dist/`, runs in browser |\n        | `onefile`                | `native=True`  | Single executable generated in `dist/`, runs in popup window |\n        | `onefile` and `windowed` | `native=True`  | Single executable generated in `dist/` (on Mac a proper `dist/myapp.app` generated incl. icon), runs in popup window, no console appears |\n        | `onefile` and `windowed` | `native=False` | Avoid (no way to exit the app) |\n        | Specify neither          |                | A `dist/myapp` directory created which can be zipped manually and distributed; run with `dist/myapp/myapp` |\n\n    - If you are using a Python virtual environment, ensure you `pip install pyinstaller` within your virtual environment\n    so that the correct PyInstaller is used, or you may get broken apps due to the wrong version of PyInstaller being picked up.\n    That is why the `nicegui-pack` invokes PyInstaller using `python -m PyInstaller` rather than just `pyinstaller`.\n",
    "format": "md",
    "demo": "",
    "url": "/documentation/section_configuration_deployment#None"
  },
  {
    "title": "Configuration & Deployment: None",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/section_configuration_deployment#None"
  },
  {
    "title": "Configuration & Deployment: ",
    "content": "\n    Note:\n    If you're getting an error \"TypeError: a bytes-like object is required, not 'str'\", try adding the following lines to the top of your `main.py` file:\n    ```py\n    import sys\n    sys.stdout = open('logs.txt', 'w')\n    ```\n    See \u003Chttps://github.com/zauberzeug/nicegui/issues/681\u003E for more information.\n",
    "format": "md",
    "demo": "",
    "url": "/documentation/section_configuration_deployment#None"
  },
  {
    "title": "Configuration & Deployment: ",
    "content": "\n    **macOS Packaging**\n\n    Add the following snippet before anything else in your main app's file, to prevent new processes from being spawned in an endless loop:\n\n    ```python\n    # macOS packaging support\n    from multiprocessing import freeze_support  # noqa\n    freeze_support()  # noqa\n\n    # all your other imports and code\n    ```\n\n    The `# noqa` comment instructs Pylance or autopep8 to not apply any PEP rule on those two lines, guaranteeing they remain on top of anything else.\n    This is key to prevent process spawning.\n",
    "format": "md",
    "demo": "",
    "url": "/documentation/section_configuration_deployment#None"
  },
  {
    "title": "Configuration & Deployment: NiceGUI On Air",
    "content": "\n    By using `ui.run(on_air=True)` you can share your local app with others over the internet 🧞.\n\n    When accessing the on-air URL, all libraries (like Vue, Quasar, ...) are loaded from our CDN.\n    Thereby only the raw content and events need to be transmitted by your local app.\n    This makes it blazing fast even if your app only has a poor internet connection (e.g. a mobile robot in the field).\n\n    By setting `on_air=True` you will get a random URL which is valid for 1 hour.\n    If you sign-up at \u003Chttps://on-air.nicegui.io\u003E, you can setup an organization and device name to get a fixed URL:\n    `https://on-air.nicegui.io/\u003Cmy-org\u003E/\u003Cmy_device_name\u003E`.\n    The device is then identified by a unique, private token which you can use instead of a boolean flag: `ui.run(on_air='\u003Cyour token\u003E')`.\n    If you [sponsor us](https://github.com/sponsors/zauberzeug),\n    we will enable multi-device management and provide built-in passphrase protection for each device.\n\n    Currently On Air is available as a tech preview and can be used free of charge.\n    We will gradually improve stability and extend the service with usage statistics, remote terminal access and more.\n    Please let us know your feedback on [GitHub](https://github.com/zauberzeug/nicegui/discussions),\n    [Reddit](https://www.reddit.com/r/nicegui/), or [Discord](https://discord.gg/TEpFeAaF4f).\n\n    **Data Privacy:**\n    We take your privacy very serious.\n    NiceGUI On Air does not log or store any content of the relayed data.\n",
    "format": "md",
    "demo": "",
    "url": "/documentation/section_configuration_deployment#nicegui_on_air"
  },
  {
    "title": "ui.badge: Badge",
    "content": "A badge element wrapping Quasar's\n`QBadge \u003Chttps://quasar.dev/vue-components/badge\u003E`_ component.\n\n:param text: the initial value of the text field\n:param color: the color name for component (either a Quasar, Tailwind, or CSS color or `None`, default: \"primary\")\n:param text_color: text color (either a Quasar, Tailwind, or CSS color or `None`, default: `None`)\n:param outline: use 'outline' design (colored text and borders only) (default: False)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.button('Click me!', on_click=lambda: badge.set_text(int(badge.text) + 1)):\n    badge = ui.badge('0', color='red').props('floating')\n\nui.run()",
    "url": "/documentation/badge#badge"
  },
  {
    "title": "ui.badge: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/badge#reference"
  },
  {
    "title": "ui.button: Button",
    "content": "This element is based on Quasar's `QBtn \u003Chttps://quasar.dev/vue-components/button\u003E`_ component.\n\nThe ``color`` parameter accepts a Quasar color, a Tailwind color, or a CSS color.\nIf a Quasar color is used, the button will be styled according to the Quasar theme including the color of the text.\nNote that there are colors like \"red\" being both a Quasar color and a CSS color.\nIn such cases the Quasar color will be used.\n\n:param text: the label of the button\n:param on_click: callback which is invoked when button is pressed\n:param color: the color of the button (either a Quasar, Tailwind, or CSS color or `None`, default: 'primary')\n:param icon: the name of an icon to be displayed on the button (default: `None`)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.button('Click me!', on_click=lambda: ui.notify('You clicked me!'))\n\nui.run()",
    "url": "/documentation/button#button"
  },
  {
    "title": "ui.button: Icons",
    "content": "You can also add an icon to a button.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.row():\n    ui.button('demo', icon='history')\n    ui.button(icon='thumb_up')\n    with ui.button():\n        ui.label('sub-elements')\n        ui.image('https://picsum.photos/id/377/640/360') \\\n            .classes('rounded-full w-16 h-16 ml-4')\n\nui.run()",
    "url": "/documentation/button#icons"
  },
  {
    "title": "ui.button: Await button click",
    "content": "Sometimes it is convenient to wait for a button click before continuing the execution.",
    "format": "md",
    "demo": "from nicegui import ui\n\n@ui.page('/')\nasync def index():\n    b = ui.button('Step')\n    await b.clicked()\n    ui.label('One')\n    await b.clicked()\n    ui.label('Two')\n    await b.clicked()\n    ui.label('Three')\n\nui.run()",
    "url": "/documentation/button#await_button_click"
  },
  {
    "title": "ui.button: Disable button with a context manager",
    "content": "This showcases a context manager that can be used to disable a button for the duration of an async process.",
    "format": "md",
    "demo": "import httpx\nfrom contextlib import contextmanager\nfrom nicegui import ui\n\n@contextmanager\ndef disable(button: ui.button):\n    button.disable()\n    try:\n        yield\n    finally:\n        button.enable()\n\nasync def get_slow_response(button: ui.button) -\u003E None:\n    with disable(button):\n        async with httpx.AsyncClient() as client:\n            response = await client.get('https://httpbin.org/delay/1', timeout=5)\n            ui.notify(f'Response code: {response.status_code}')\n\nui.button('Get slow response', on_click=lambda e: get_slow_response(e.sender))\n\nui.run()",
    "url": "/documentation/button#disable_button_with_a_context_manager"
  },
  {
    "title": "ui.button: Custom toggle button",
    "content": "As with all other elements, you can implement your own subclass with specialized logic.\nLike this red/green toggle button with an internal boolean state.",
    "format": "md",
    "demo": "from nicegui import ui\n\nclass ToggleButton(ui.button):\n\n    def __init__(self, *args, **kwargs) -\u003E None:\n        super().__init__(*args, **kwargs)\n        self._state = False\n        self.on('click', self.toggle)\n\n    def toggle(self) -\u003E None:\n        \"\"\"Toggle the button state.\"\"\"\n        self._state = not self._state\n        self.update()\n\n    def update(self) -\u003E None:\n        self.props(f'color={\"green\" if self._state else \"red\"}')\n        super().update()\n\nToggleButton('Toggle me')\n\nui.run()",
    "url": "/documentation/button#custom_toggle_button"
  },
  {
    "title": "ui.button: Floating Action Button",
    "content": "As described in the [Quasar documentation](https://quasar.dev/vue-components/floating-action-button),\na Floating Action Button (FAB) is simply a \"page-sticky\" with a button inside.\nWith the \"fab\" prop, the button will be rounded and gets a shadow.\nColor can be freely chosen, but most often it is an accent color.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.colors(accent='#6AD4DD')\nwith ui.page_sticky(x_offset=18, y_offset=18):\n    ui.button(icon='home', on_click=lambda: ui.notify('home')) \\\n        .props('fab color=accent')\n\nui.run()",
    "url": "/documentation/button#floating_action_button"
  },
  {
    "title": "ui.button: Expandable Floating Action Button",
    "content": "\n    To create a Floating Action Button (FAB) with multiple actions that are revealed when the FAB is clicked,\n    you can use [`ui.fab` and `ui.fab_action`](fab) elements,\n    which are based on [Quasar's QFab component](https://quasar.dev/vue-components/floating-action-button).\n",
    "format": "md",
    "demo": "",
    "url": "/documentation/button#expandable_floating_action_button"
  },
  {
    "title": "ui.button: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/button#reference"
  },
  {
    "title": "ui.dropdown_button: Dropdown Button",
    "content": "This element is based on Quasar's `QBtnDropDown \u003Chttps://quasar.dev/vue-components/button-dropdown\u003E`_ component.\n\nThe ``color`` parameter accepts a Quasar color, a Tailwind color, or a CSS color.\nIf a Quasar color is used, the button will be styled according to the Quasar theme including the color of the text.\nNote that there are colors like \"red\" being both a Quasar color and a CSS color.\nIn such cases the Quasar color will be used.\n\n:param text: the label of the button\n:param value: if the dropdown is open or not (default: `False`)\n:param on_value_change: callback which is invoked when the dropdown is opened or closed\n:param on_click: callback which is invoked when button is pressed\n:param color: the color of the button (either a Quasar, Tailwind, or CSS color or `None`, default: 'primary')\n:param icon: the name of an icon to be displayed on the button (default: `None`)\n:param auto_close: whether the dropdown should close automatically when an item is clicked (default: `False`)\n:param split: whether to split the dropdown icon into a separate button (default: `False`)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.dropdown_button('Open me!', auto_close=True):\n    ui.item('Item 1', on_click=lambda: ui.notify('You clicked item 1'))\n    ui.item('Item 2', on_click=lambda: ui.notify('You clicked item 2'))\n\nui.run()",
    "url": "/documentation/button_dropdown#dropdown_button"
  },
  {
    "title": "ui.dropdown_button: Custom elements inside dropdown button",
    "content": "You can put any elements inside a dropdown button.\nHere is a demo with a few switches.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.dropdown_button('Settings', icon='settings', split=True):\n    with ui.row().classes('p-4 items-center'):\n        ui.icon('volume_up', size='sm')\n        ui.switch().props('color=negative')\n        ui.separator().props('vertical')\n        ui.icon('mic', size='sm')\n        ui.switch().props('color=negative')\n\nui.run()",
    "url": "/documentation/button_dropdown#custom_elements_inside_dropdown_button"
  },
  {
    "title": "ui.dropdown_button: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/button_dropdown#reference"
  },
  {
    "title": "ui.button_group: Button Group",
    "content": "This element is based on Quasar's `QBtnGroup \u003Chttps://quasar.dev/vue-components/button-group\u003E`_ component.\nYou must use the same design props on both the parent button group and the children buttons.\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.button_group():\n    ui.button('One', on_click=lambda: ui.notify('You clicked Button 1!'))\n    ui.button('Two', on_click=lambda: ui.notify('You clicked Button 2!'))\n    ui.button('Three', on_click=lambda: ui.notify('You clicked Button 3!'))\n\nui.run()",
    "url": "/documentation/button_group#button_group"
  },
  {
    "title": "ui.button_group: Button group with dropdown button",
    "content": "You can also add a dropdown button to a button group.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.button_group():\n    ui.button('One')\n    ui.button('Two')\n    with ui.dropdown_button('Dropdown'):\n        ui.item('Item 1', on_click=lambda: ui.notify('Item 1'))\n        ui.item('Item 2', on_click=lambda: ui.notify('Item 2'))\n\nui.run()",
    "url": "/documentation/button_group#button_group_with_dropdown_button"
  },
  {
    "title": "ui.button_group: Button group styling",
    "content": "You can apply the same styling options to a button group as to a button, like \"flat\", \"outline\", \"push\", ...\nHowever, you must always use the same design props for the button group and its containing buttons.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.button_group().props('rounded'):\n    ui.button('One')\n    ui.button('Two')\n    ui.button('Three')\nwith ui.button_group().props('push glossy'):\n    ui.button('One', color='red').props('push')\n    ui.button('Two', color='orange').props('push text-color=black')\n    ui.button('Three', color='yellow').props('push text-color=black')\nwith ui.button_group().props('outline'):\n    ui.button('One').props('outline')\n    ui.button('Two').props('outline')\n    ui.button('Three').props('outline')\n\nui.run()",
    "url": "/documentation/button_group#button_group_styling"
  },
  {
    "title": "ui.button_group: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/button_group#reference"
  },
  {
    "title": "ui.checkbox: Checkbox",
    "content": "This element is based on Quasar's `QCheckbox \u003Chttps://quasar.dev/vue-components/checkbox\u003E`_ component.\n\n:param text: the label to display next to the checkbox\n:param value: whether it should be checked initially (default: `False`)\n:param on_change: callback to execute when value changes\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\ncheckbox = ui.checkbox('check me')\nui.label('Check!').bind_visibility_from(checkbox, 'value')\n\nui.run()",
    "url": "/documentation/checkbox#checkbox"
  },
  {
    "title": "ui.checkbox: Handle User Interaction",
    "content": "The `on_change` function passed via parameter will be called when the checkbox is clicked\n*and* when the value changes via `set_value` call.\nTo execute a function only when the user interacts with the checkbox, you can use the generic `on` method.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.row():\n    c1 = ui.checkbox(on_change=lambda e: ui.notify(str(e.value)))\n    ui.button('set value', on_click=lambda: c1.set_value(not c1.value))\nwith ui.row():\n    c2 = ui.checkbox().on('click', lambda e: ui.notify(str(e.sender.value)))\n    ui.button('set value', on_click=lambda: c2.set_value(not c2.value))\n\nui.run()",
    "url": "/documentation/checkbox#handle_user_interaction"
  },
  {
    "title": "ui.checkbox: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/checkbox#reference"
  },
  {
    "title": "ui.codemirror: CodeMirror",
    "content": "An element to create a code editor using `CodeMirror \u003Chttps://codemirror.net/\u003E`_.\n\nIt supports syntax highlighting for over 140 languages, more than 30 themes, line numbers, code folding, (limited) auto-completion, and more.\n\nSupported languages and themes:\n    - Languages: A list of supported languages can be found in the `@codemirror/language-data \u003Chttps://github.com/codemirror/language-data/blob/main/src/language-data.ts\u003E`_ package.\n    - Themes: A list can be found in the `@uiw/codemirror-themes-all \u003Chttps://github.com/uiwjs/react-codemirror/tree/master/themes/all\u003E`_ package.\n\nAt runtime, the methods `supported_languages` and `supported_themes` can be used to get supported languages and themes.\n\n:param value: initial value of the editor (default: \"\")\n:param on_change: callback to be executed when the value changes (default: `None`)\n:param language: initial language of the editor (case-insensitive, default: `None`)\n:param theme: initial theme of the editor (default: \"basicLight\")\n:param indent: string to use for indentation (any string consisting entirely of the same whitespace character, default: \"    \")\n:param line_wrapping: whether to wrap lines (default: `False`)\n:param highlight_whitespace: whether to highlight whitespace (default: `False`)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\neditor = ui.codemirror('print(\"Edit me!\")', language='Python').classes('h-32')\nui.select(editor.supported_languages, label='Language', clearable=True) \\\n    .classes('w-32').bind_value(editor, 'language')\nui.select(editor.supported_themes, label='Theme') \\\n    .classes('w-32').bind_value(editor, 'theme')\n\nui.run()",
    "url": "/documentation/codemirror#codemirror"
  },
  {
    "title": "ui.codemirror: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/codemirror#reference"
  },
  {
    "title": "ui.chip: Chip",
    "content": "A chip element wrapping Quasar's `QChip \u003Chttps://quasar.dev/vue-components/chip\u003E`_ component.\nIt can be clickable, selectable and removable.\n\n:param text: the initial value of the text field (default: \"\")\n:param icon: the name of an icon to be displayed on the chip (default: `None`)\n:param color: the color name for component (either a Quasar, Tailwind, or CSS color or `None`, default: \"primary\")\n:param text_color: text color (either a Quasar, Tailwind, or CSS color or `None`, default: `None`)\n:param on_click: callback which is invoked when chip is clicked. Makes the chip clickable if set\n:param selectable: whether the chip is selectable (default: `False`)\n:param selected: whether the chip is selected (default: `False`)\n:param on_selection_change: callback which is invoked when the chip's selection state is changed\n:param removable: whether the chip is removable. Shows a small \"x\" button if True (default: `False`)\n:param on_value_change: callback which is invoked when the chip is removed or unremoved\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.row().classes('gap-1'):\n    ui.chip('Click me', icon='ads_click', on_click=lambda: ui.notify('Clicked'))\n    ui.chip('Selectable', selectable=True, icon='bookmark', color='orange')\n    ui.chip('Removable', removable=True, icon='label', color='indigo-3')\n    ui.chip('Styled', icon='star', color='green').props('outline square')\n    ui.chip('Disabled', icon='block', color='red').set_enabled(False)\n\nui.run()",
    "url": "/documentation/chip#chip"
  },
  {
    "title": "ui.chip: Dynamic chip elements as labels/tags",
    "content": "This demo shows how to implement a dynamic list of chips as labels or tags.\nYou can add new chips by typing a label and pressing Enter or pressing the plus button.\nRemoved chips still exist, but their value is set to `False`.",
    "format": "md",
    "demo": "from nicegui import ui\n\ndef add_chip():\n    with chips:\n        ui.chip(label_input.value, icon='label', color='silver', removable=True)\n    label_input.value = ''\n\nlabel_input = ui.input('Add label').on('keydown.enter', add_chip)\nwith label_input.add_slot('append'):\n    ui.button(icon='add', on_click=add_chip).props('round dense flat')\n\nwith ui.row().classes('gap-0') as chips:\n    ui.chip('Label 1', icon='label', color='silver', removable=True)\n\nui.button('Restore removed chips', icon='unarchive',\n          on_click=lambda: [chip.set_value(True) for chip in chips]) \\\n    .props('flat')\n\nui.run()",
    "url": "/documentation/chip#dynamic_chip_elements_as_labels_tags"
  },
  {
    "title": "ui.chip: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/chip#reference"
  },
  {
    "title": "ui.color_input: Color Input",
    "content": "This element extends Quasar's `QInput \u003Chttps://quasar.dev/vue-components/input\u003E`_ component with a color picker.\n\n:param label: displayed label for the color input\n:param placeholder: text to show if no color is selected\n:param value: the current color value\n:param on_change: callback to execute when the value changes\n:param preview: change button background to selected color (default: False)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nlabel = ui.label('Change my color!')\nui.color_input(label='Color', value='#000000',\n               on_change=lambda e: label.style(f'color:{e.value}'))\n\nui.run()",
    "url": "/documentation/color_input#color_input"
  },
  {
    "title": "ui.color_input: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/color_input#reference"
  },
  {
    "title": "ui.color_picker: Color Picker",
    "content": "This element is based on Quasar's `QMenu \u003Chttps://quasar.dev/vue-components/menu\u003E`_ and\n`QColor \u003Chttps://quasar.dev/vue-components/color-picker\u003E`_ components.\n\n:param on_pick: callback to execute when a color is picked\n:param value: whether the menu is already opened (default: `False`)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.button(icon='colorize') as button:\n    ui.color_picker(on_pick=lambda e: button.classes(f'!bg-[{e.color}]'))\n\nui.run()",
    "url": "/documentation/color_picker#color_picker"
  },
  {
    "title": "ui.color_picker: Customize the Color Picker",
    "content": "You can customize the color picker via props, classes and style attributes.\nBecause the QColor component is nested inside a menu, you can't use the `props` method directly,\nbut via the `q_color` attribute.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.button(icon='palette'):\n    picker = ui.color_picker(on_pick=lambda e: ui.notify(f'You chose {e.color}'))\n    picker.q_color.props('default-view=palette no-header no-footer')\n\nui.run()",
    "url": "/documentation/color_picker#customize_the_color_picker"
  },
  {
    "title": "ui.color_picker: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/color_picker#reference"
  },
  {
    "title": "ui.date: Date Input",
    "content": "This element is based on Quasar's `QDate \u003Chttps://quasar.dev/vue-components/date\u003E`_ component.\nThe date is a string in the format defined by the `mask` parameter.\n\nYou can also use the `range` or `multiple` props to select a range of dates or multiple dates::\n\n    ui.date({'from': '2023-01-01', 'to': '2023-01-05'}).props('range')\n    ui.date(['2023-01-01', '2023-01-02', '2023-01-03']).props('multiple')\n    ui.date([{'from': '2023-01-01', 'to': '2023-01-05'}, '2023-01-07']).props('multiple range')\n\n:param value: the initial date\n:param mask: the format of the date string (default: 'YYYY-MM-DD')\n:param on_change: callback to execute when changing the date\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.date(value='2023-01-01', on_change=lambda e: result.set_text(e.value))\nresult = ui.label()\n\nui.run()",
    "url": "/documentation/date#date_input"
  },
  {
    "title": "ui.date: Input element with date picker",
    "content": "This demo shows how to implement a date picker with an input element.\nWe place an icon in the input element's append slot.\nWhen the icon is clicked, we open a menu with a date picker.\n[QMenu](https://quasar.dev/vue-components/menu)'s \"no-parent-event\" prop is used\nto prevent opening the menu when clicking into the input field.\nAs the menu doesn't come with a \"Close\" button by default, we add one for convenience.\n\nThe date is bound to the input element's value.\nSo both the input element and the date picker will stay in sync whenever the date is changed.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.input('Date') as date:\n    with ui.menu().props('no-parent-event') as menu:\n        with ui.date().bind_value(date):\n            with ui.row().classes('justify-end'):\n                ui.button('Close', on_click=menu.close).props('flat')\n    with date.add_slot('append'):\n        ui.icon('edit_calendar').on('click', menu.open).classes('cursor-pointer')\n\nui.run()",
    "url": "/documentation/date#input_element_with_date_picker"
  },
  {
    "title": "ui.date: Date range input",
    "content": "You can use the \"range\" prop to select a range of dates.\nThe `value` will be a dictionary with \"from\" and \"to\" keys.\nThe following demo shows how to bind a date range picker to an input element,\nusing the `forward` and `backward` functions to convert between the date picker's dictionary and the input string.",
    "format": "md",
    "demo": "from nicegui import ui\n\ndate_input = ui.input('Date range').classes('w-40')\nui.date().props('range').bind_value(\n    date_input,\n    forward=lambda x: f'{x[\"from\"]} - {x[\"to\"]}' if x else None,\n    backward=lambda x: {\n        'from': x.split(' - ')[0],\n        'to': x.split(' - ')[1],\n    } if ' - ' in (x or '') else None,\n)\n\nui.run()",
    "url": "/documentation/date#date_range_input"
  },
  {
    "title": "ui.date: Date filter",
    "content": "This demo shows how to filter the dates in a date picker.\nIn order to pass a function to the date picker, we use the `:options` property.\nThe leading `:` tells NiceGUI that the value is a JavaScript expression.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.date().props('''default-year-month=2023/01 :options=\"date =\u003E date \u003C= '2023/01/15'\"''')\n\nui.run()",
    "url": "/documentation/date#date_filter"
  },
  {
    "title": "ui.date: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/date#reference"
  },
  {
    "title": "ui.fab: Floating Action Button (FAB)",
    "content": "A floating action button that can be used to trigger an action.\nThis element is based on Quasar's `QFab \u003Chttps://quasar.dev/vue-components/floating-action-button#qfab-api\u003E`_ component.\n\n:param icon: icon to be displayed on the FAB\n:param value: whether the FAB is already opened (default: ``False``)\n:param label: optional label for the FAB\n:param color: background color of the FAB (default: \"primary\")\n:param direction: direction of the FAB (\"up\", \"down\", \"left\", \"right\", default: \"right\")\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.fab('navigation', label='Transport'):\n    ui.fab_action('train', on_click=lambda: ui.notify('Train'))\n    ui.fab_action('sailing', on_click=lambda: ui.notify('Boat'))\n    ui.fab_action('rocket', on_click=lambda: ui.notify('Rocket'))\n\nui.run()",
    "url": "/documentation/fab#floating_action_button_(fab)"
  },
  {
    "title": "ui.fab: Styling",
    "content": "You can style the FAB and its actions using the `color` parameter.\nThe `color` parameter accepts a Quasar color, a Tailwind color, or a CSS color.\nYou can also change the direction of the FAB using the `direction` parameter.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.fab('shopping_cart', label='Shop', color='teal', direction='up') \\\n        .classes('mt-40 mx-auto'):\n    ui.fab_action('sym_o_nutrition', label='Fruits', color='green')\n    ui.fab_action('local_pizza', label='Pizza', color='yellow')\n    ui.fab_action('sym_o_icecream', label='Ice Cream', color='orange')\n\nui.run()",
    "url": "/documentation/fab#styling"
  },
  {
    "title": "ui.fab: Reference for ui.fab",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/fab#reference_for_ui_fab"
  },
  {
    "title": "ui.fab: Reference for ui.fab_action",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/fab#reference_for_ui_fab_action"
  },
  {
    "title": "ui.input_chips: Input Chips",
    "content": "An input field that manages a collection of values as visual \"chips\" or tags.\nUsers can type to add new chips and remove existing ones by clicking or using keyboard shortcuts.\n\nThis element is based on Quasar's `QSelect \u003Chttps://quasar.dev/vue-components/select\u003E`_ component.\nUnlike a traditional dropdown selection, this variant focuses on free-form text input with chips,\nmaking it ideal for tags, keywords, or any list of user-defined values.\n\nYou can use the ``validation`` parameter to define a dictionary of validation rules,\ne.g. ``{'Too long!': lambda value: len(value) \u003C 3}``.\nThe key of the first rule that fails will be displayed as an error message.\nAlternatively, you can pass a callable that returns an optional error message.\nTo disable the automatic validation on every value change, you can use the `without_auto_validation` method.\n\n*Added in version 2.22.0*\n\n:param label: the label to display above the selection\n:param value: the initial value\n:param on_change: callback to execute when selection changes\n:param new_value_mode: handle new values from user input (default: \"toggle\")\n:param clearable: whether to add a button to clear the selection\n:param validation: dictionary of validation rules or a callable that returns an optional error message (default: None for no validation)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.input_chips('My favorite chips', value=['Pringles', 'Doritos', \"Lay's\"])\n\nui.run()",
    "url": "/documentation/input_chips#input_chips"
  },
  {
    "title": "ui.input_chips: New-value modes",
    "content": "There are three new-value modes: \"add\", \"add-unique\", and \"toggle\" (the default).\n\n- \"add\" adds all values to the list (allowing duplicates).\n- \"add-unique\" adds only unique values to the list.\n- \"toggle\" adds or removes the value (based on if it exists or not in the list).",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.input_chips('Add', new_value_mode='add')\nui.input_chips('Add unique', new_value_mode='add-unique')\nui.input_chips('Toggle', new_value_mode='toggle')\n\nui.run()",
    "url": "/documentation/input_chips#new-value_modes"
  },
  {
    "title": "ui.input_chips: Auto-split values",
    "content": "This demo shows how to automatically split values when the user enters comma-separated values.",
    "format": "md",
    "demo": "from nicegui import events, ui\n\ndef split_values(e: events.ValueChangeEventArguments):\n    for value in e.value[:]:\n        e.value.remove(value)\n        e.value.extend(value.split(','))\n\nui.input_chips(on_change=split_values)\nui.label('Try entering \"x,y,z\"!')\n\nui.run()",
    "url": "/documentation/input_chips#auto-split_values"
  },
  {
    "title": "ui.input_chips: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/input_chips#reference"
  },
  {
    "title": "ui.input: Text Input",
    "content": "This element is based on Quasar's `QInput \u003Chttps://quasar.dev/vue-components/input\u003E`_ component.\n\nThe `on_change` event is called on every keystroke and the value updates accordingly.\nIf you want to wait until the user confirms the input, you can register a custom event callback, e.g.\n`ui.input(...).on('keydown.enter', ...)` or `ui.input(...).on('blur', ...)`.\n\nYou can use the `validation` parameter to define a dictionary of validation rules,\ne.g. ``{'Too long!': lambda value: len(value) \u003C 3}``.\nThe key of the first rule that fails will be displayed as an error message.\nAlternatively, you can pass a callable that returns an optional error message.\nTo disable the automatic validation on every value change, you can use the `without_auto_validation` method.\n\nNote about styling the input:\nQuasar's `QInput` component is a wrapper around a native `input` element.\nThis means that you cannot style the input directly,\nbut you can use the `input-class` and `input-style` props to style the native input element.\nSee the \"Style\" props section on the `QInput \u003Chttps://quasar.dev/vue-components/input\u003E`_ documentation for more details.\n\n:param label: displayed label for the text input\n:param placeholder: text to show if no value is entered\n:param value: the current value of the text input\n:param password: whether to hide the input (default: False)\n:param password_toggle_button: whether to show a button to toggle the password visibility (default: False)\n:param on_change: callback to execute when the value changes\n:param autocomplete: optional list of strings for autocompletion\n:param validation: dictionary of validation rules or a callable that returns an optional error message (default: None for no validation)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.input(label='Text', placeholder='start typing',\n         on_change=lambda e: result.set_text('you typed: ' + e.value),\n         validation={'Input too long': lambda value: len(value) \u003C 20})\nresult = ui.label()\n\nui.run()",
    "url": "/documentation/input#text_input"
  },
  {
    "title": "ui.input: Autocompletion",
    "content": "The `autocomplete` feature provides suggestions as you type, making input easier and faster.\nThe parameter `options` is a list of strings that contains the available options that will appear.",
    "format": "md",
    "demo": "from nicegui import ui\n\noptions = ['AutoComplete', 'NiceGUI', 'Awesome']\nui.input(label='Text', placeholder='start typing', autocomplete=options)\n\nui.run()",
    "url": "/documentation/input#autocompletion"
  },
  {
    "title": "ui.input: Clearable",
    "content": "The `clearable` prop from [Quasar](https://quasar.dev/) adds a button to the input that clears the text.",
    "format": "md",
    "demo": "from nicegui import ui\n\ni = ui.input(value='some text').props('clearable')\nui.label().bind_text_from(i, 'value')\n\nui.run()",
    "url": "/documentation/input#clearable"
  },
  {
    "title": "ui.input: Styling",
    "content": "Quasar has a lot of [props to change the appearance](https://quasar.dev/vue-components/input).\nIt is even possible to style the underlying input with `input-style` and `input-class` props\nand use the provided slots to add custom elements.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.input(placeholder='start typing').props('rounded outlined dense')\nui.input('styling', value='some text') \\\n    .props('input-style=\"color: blue\" input-class=\"font-mono\"')\nwith ui.input(value='custom clear button').classes('w-64') as i:\n    ui.button(color='orange-8', on_click=lambda: i.set_value(None), icon='delete') \\\n        .props('flat dense').bind_visibility_from(i, 'value')\n\nui.run()",
    "url": "/documentation/input#styling"
  },
  {
    "title": "ui.input: Input validation",
    "content": "You can validate the input in two ways:\n\n- by passing a callable that returns an error message or `None`, or\n- by passing a dictionary that maps error messages to callables that return `True` if the input is valid.\n\n*Since version 2.7.0:*\nThe callable validation function can also be an async coroutine.\nIn this case, the validation is performed asynchronously in the background.\n\nYou can use the `validate` method of the input element to trigger the validation manually.\nIt returns `True` if the input is valid, and an error message otherwise.\nFor async validation functions, the return value must be explicitly disabled by setting `return_result=False`.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.input('Name', validation=lambda value: 'Too short' if len(value) \u003C 5 else None)\nui.input('Name', validation={'Too short': lambda value: len(value) \u003E= 5})\n\nui.run()",
    "url": "/documentation/input#input_validation"
  },
  {
    "title": "ui.input: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/input#reference"
  },
  {
    "title": "ui.joystick: Joystick",
    "content": "Create a joystick based on `nipple.js \u003Chttps://yoannmoi.net/nipplejs/\u003E`_.\n\n:param on_start: callback for when the user touches the joystick\n:param on_move: callback for when the user moves the joystick\n:param on_end: callback for when the user releases the joystick\n:param throttle: throttle interval in seconds for the move event (default: 0.05)\n:param options: arguments like `color` which should be passed to the `underlying nipple.js library \u003Chttps://github.com/yoannmoinet/nipplejs#options\u003E`_\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.joystick(\n    color='blue', size=50,\n    on_move=lambda e: coordinates.set_text(f'{e.x:.3f}, {e.y:.3f}'),\n    on_end=lambda _: coordinates.set_text('0, 0'),\n).classes('bg-slate-300')\ncoordinates = ui.label('0, 0')\n\nui.run()",
    "url": "/documentation/joystick#joystick"
  },
  {
    "title": "ui.joystick: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/joystick#reference"
  },
  {
    "title": "ui.knob: Knob",
    "content": "This element is based on Quasar's `QKnob \u003Chttps://quasar.dev/vue-components/knob\u003E`_ component.\nThe element is used to take a number input from the user through mouse/touch panning.\n\n:param value: the initial value (default: 0.0)\n:param min: the minimum value (default: 0.0)\n:param max: the maximum value (default: 1.0)\n:param step: the step size (default: 0.01)\n:param color: knob color (either a Quasar, Tailwind, or CSS color or `None`, default: \"primary\")\n:param center_color: color name for the center part of the component, examples: primary, teal-10\n:param track_color: color name for the track of the component, examples: primary, teal-10\n:param size: size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl), examples: 16px, 2rem\n:param show_value: whether to show the value as text\n:param on_change: callback to execute when the value changes\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nknob = ui.knob(0.3, show_value=True)\n\nwith ui.knob(color='orange', track_color='grey-2').bind_value(knob, 'value'):\n    ui.icon('volume_up')\n\nui.run()",
    "url": "/documentation/knob#knob"
  },
  {
    "title": "ui.knob: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/knob#reference"
  },
  {
    "title": "ui.number: Number Input",
    "content": "This element is based on Quasar's `QInput \u003Chttps://quasar.dev/vue-components/input\u003E`_ component.\n\nYou can use the `validation` parameter to define a dictionary of validation rules,\ne.g. ``{'Too small!': lambda value: value \u003E 3}``.\nThe key of the first rule that fails will be displayed as an error message.\nAlternatively, you can pass a callable that returns an optional error message.\nTo disable the automatic validation on every value change, you can use the `without_auto_validation` method.\n\n:param label: displayed name for the number input\n:param placeholder: text to show if no value is entered\n:param value: the initial value of the field\n:param min: the minimum value allowed\n:param max: the maximum value allowed\n:param precision: the number of decimal places allowed (default: no limit, negative: decimal places before the dot)\n:param step: the step size for the stepper buttons\n:param prefix: a prefix to prepend to the displayed value\n:param suffix: a suffix to append to the displayed value\n:param format: a string like \"%.2f\" to format the displayed value\n:param on_change: callback to execute when the value changes\n:param validation: dictionary of validation rules or a callable that returns an optional error message (default: None for no validation)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.number(label='Number', value=3.1415927, format='%.2f',\n          on_change=lambda e: result.set_text(f'you entered: {e.value}'))\nresult = ui.label()\n\nui.run()",
    "url": "/documentation/number#number_input"
  },
  {
    "title": "ui.number: Clearable",
    "content": "The `clearable` prop from [Quasar](https://quasar.dev/) adds a button to the input that clears the text.",
    "format": "md",
    "demo": "from nicegui import ui\n\ni = ui.number(value=42).props('clearable')\nui.label().bind_text_from(i, 'value')\n\nui.run()",
    "url": "/documentation/number#clearable"
  },
  {
    "title": "ui.number: Number of decimal places",
    "content": "You can specify the number of decimal places using the `precision` parameter.\nA negative value means decimal places before the dot.\nThe rounding takes place when the input loses focus,\nwhen sanitization parameters like min, max or precision change,\nor when `sanitize()` is called manually.",
    "format": "md",
    "demo": "from nicegui import ui\n\nn = ui.number(value=3.14159265359, precision=5)\nn.sanitize()\n\nui.run()",
    "url": "/documentation/number#number_of_decimal_places"
  },
  {
    "title": "ui.number: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/number#reference"
  },
  {
    "title": "ui.radio: Radio Selection",
    "content": "This element is based on Quasar's `QRadio \u003Chttps://quasar.dev/vue-components/radio\u003E`_ component.\n\nThe options can be specified as a list of values, or as a dictionary mapping values to labels.\nAfter manipulating the options, call `update()` to update the options in the UI.\n\n:param options: a list ['value1', ...] or dictionary `{'value1':'label1', ...}` specifying the options\n:param value: the initial value\n:param on_change: callback to execute when selection changes\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nradio1 = ui.radio([1, 2, 3], value=1).props('inline')\nradio2 = ui.radio({1: 'A', 2: 'B', 3: 'C'}).props('inline').bind_value(radio1, 'value')\n\nui.run()",
    "url": "/documentation/radio#radio_selection"
  },
  {
    "title": "ui.radio: Inject arbitrary content",
    "content": "Thanks to the [`ui.teleport` element](teleport), you can use arbitrary content for the radio options.",
    "format": "md",
    "demo": "from nicegui import ui\n\noptions = ['Star', 'Thump Up', 'Heart']\nradio = ui.radio({x: '' for x in options}, value='Star').props('inline')\nwith ui.teleport(f'#{radio.html_id} \u003E div:nth-child(1) .q-radio__label'):\n    ui.icon('star', size='md')\nwith ui.teleport(f'#{radio.html_id} \u003E div:nth-child(2) .q-radio__label'):\n    ui.icon('thumb_up', size='md')\nwith ui.teleport(f'#{radio.html_id} \u003E div:nth-child(3) .q-radio__label'):\n    ui.icon('favorite', size='md')\nui.label().bind_text_from(radio, 'value')\n\nui.run()",
    "url": "/documentation/radio#inject_arbitrary_content"
  },
  {
    "title": "ui.radio: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/radio#reference"
  },
  {
    "title": "ui.range: Range",
    "content": "This element is based on Quasar's `QRange \u003Chttps://quasar.dev/vue-components/range\u003E`_ component.\n\n:param min: lower bound of the range\n:param max: upper bound of the range\n:param step: step size\n:param value: initial value to set min and max position of the range\n:param on_change: callback which is invoked when the user releases the range\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nmin_max_range = ui.range(min=0, max=100, value={'min': 20, 'max': 80})\nui.label().bind_text_from(min_max_range, 'value',\n                          backward=lambda v: f'min: {v[\"min\"]}, max: {v[\"max\"]}')\n\nui.run()",
    "url": "/documentation/range#range"
  },
  {
    "title": "ui.range: Customize labels",
    "content": "You can customize the colors of the range and its labels by setting them individually or for the range in total.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.label('Color the entire range')\nui.range(min=0, max=100, value={'min': 20, 'max': 80}) \\\n    .props('label snap color=\"secondary\"')\n\nui.label('Customize the color of the labels')\nui.range(min=0, max=100, value={'min': 40, 'max': 80}) \\\n    .props('label-always snap label-color=\"secondary\" right-label-text-color=\"black\"')\n\nui.run()",
    "url": "/documentation/range#customize_labels"
  },
  {
    "title": "ui.range: Change range limits",
    "content": "This demo shows how to change the limits on the click of a button.",
    "format": "md",
    "demo": "from nicegui import ui\n\ndef increase_limits():\n    r.min -= 10\n    r.max += 10\n\nui.button('Increase limits', on_click=increase_limits)\nr = ui.range(min=0, max=100, value={'min': 30, 'max': 70}).props('label-always')\n\nui.run()",
    "url": "/documentation/range#change_range_limits"
  },
  {
    "title": "ui.range: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/range#reference"
  },
  {
    "title": "ui.rating: Rating",
    "content": "This element is based on Quasar's `QRating \u003Chttps://quasar.dev/vue-components/rating\u003E`_ component.\n\n*Added in version 2.12.0*\n\n:param value: initial value (default: ``None``)\n:param max: maximum rating, number of icons (default: 5)\n:param icon: name of icons to be displayed (default: star)\n:param icon_selected: name of an icon to be displayed when selected (default: same as ``icon``)\n:param icon_half: name of an icon to be displayed when half-selected (default: same as ``icon``)\n:param color: color(s) of the icons (Quasar, Tailwind, or CSS colors or ``None``, default: \"primary\")\n:param size: size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl), examples: 16px, 2rem\n:param on_change: callback to execute when selection changes\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.rating(value=4)\n\nui.run()",
    "url": "/documentation/rating#rating"
  },
  {
    "title": "ui.rating: Customize icons",
    "content": "You can customize name and size of the icons.\nOptionally, unselected, selected or half-selected values can have different icons.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.rating(\n    value=3.5,\n    size='lg',\n    icon='sentiment_dissatisfied',\n    icon_selected='sentiment_satisfied',\n    icon_half='sentiment_neutral',\n)\nui.rating(\n    value=3.5,\n    size='lg',\n    icon='star',\n    icon_selected='star',\n    icon_half='star_half',\n)\n\nui.run()",
    "url": "/documentation/rating#customize_icons"
  },
  {
    "title": "ui.rating: Customize color",
    "content": "You can customize the color of the rating either by providing a single color or a range of different colors.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.rating(value=3, color='red-10')\nui.rating(value=5, color=['green-2', 'green-4', 'green-6', 'green-8', 'green-10'])\n\nui.run()",
    "url": "/documentation/rating#customize_color"
  },
  {
    "title": "ui.rating: Maximum rating",
    "content": "This demo shows how to change the maximum possible rating\nas well as binding the value to a slider.",
    "format": "md",
    "demo": "from nicegui import ui\n\nslider = ui.slider(value=5, min=0, max=10)\nui.rating(max=10, icon='circle').bind_value(slider)\n\nui.run()",
    "url": "/documentation/rating#maximum_rating"
  },
  {
    "title": "ui.rating: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/rating#reference"
  },
  {
    "title": "ui.select: Dropdown Selection",
    "content": "This element is based on Quasar's `QSelect \u003Chttps://quasar.dev/vue-components/select\u003E`_ component.\n\nThe options can be specified as a list of values, or as a dictionary mapping values to labels.\nAfter manipulating the options, call `update()` to update the options in the UI.\n\nIf `with_input` is True, an input field is shown to filter the options.\n\nIf `new_value_mode` is not None, it implies `with_input=True` and the user can enter new values in the input field.\nSee `Quasar's documentation \u003Chttps://quasar.dev/vue-components/select#the-new-value-mode-prop\u003E`_ for details.\nNote that this mode is ineffective when setting the `value` property programmatically.\n\nYou can use the `validation` parameter to define a dictionary of validation rules,\ne.g. ``{'Too long!': lambda value: len(value) \u003C 3}``.\nThe key of the first rule that fails will be displayed as an error message.\nAlternatively, you can pass a callable that returns an optional error message.\nTo disable the automatic validation on every value change, you can use the `without_auto_validation` method.\n\n:param options: a list ['value1', ...] or dictionary `{'value1':'label1', ...}` specifying the options\n:param label: the label to display above the selection\n:param value: the initial value\n:param on_change: callback to execute when selection changes\n:param with_input: whether to show an input field to filter the options\n:param new_value_mode: handle new values from user input (default: None, i.e. no new values)\n:param multiple: whether to allow multiple selections\n:param clearable: whether to add a button to clear the selection\n:param validation: dictionary of validation rules or a callable that returns an optional error message (default: None for no validation)\n:param key_generator: a callback or iterator to generate a dictionary key for new values\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nselect1 = ui.select([1, 2, 3], value=1)\nselect2 = ui.select({1: 'One', 2: 'Two', 3: 'Three'}).bind_value(select1, 'value')\n\nui.run()",
    "url": "/documentation/select#dropdown_selection"
  },
  {
    "title": "ui.select: Search-as-you-type",
    "content": "You can activate `with_input` to get a text input with autocompletion.\nThe options will be filtered as you type.",
    "format": "md",
    "demo": "from nicegui import ui\n\ncontinents = [\n    'Asia',\n    'Africa',\n    'Antarctica',\n    'Europe',\n    'Oceania',\n    'North America',\n    'South America',\n]\nui.select(options=continents, with_input=True,\n          on_change=lambda e: ui.notify(e.value)).classes('w-40')\n\nui.run()",
    "url": "/documentation/select#search-as-you-type"
  },
  {
    "title": "ui.select: Multi selection",
    "content": "You can activate `multiple` to allow the selection of more than one item.",
    "format": "md",
    "demo": "from nicegui import ui\n\nnames = ['Alice', 'Bob', 'Carol']\nui.select(names, multiple=True, value=names[:2], label='comma-separated') \\\n    .classes('w-64')\nui.select(names, multiple=True, value=names[:2], label='with chips') \\\n    .classes('w-64').props('use-chips')\n\nui.run()",
    "url": "/documentation/select#multi_selection"
  },
  {
    "title": "ui.select: Update options",
    "content": "Options can be changed with the `options` property.\nBut then you also need to call `update()` afterwards to let the change take effect.\n`set_options` is a shortcut that does both and works well for lambdas.",
    "format": "md",
    "demo": "from nicegui import ui\n\nselect = ui.select([1, 2, 3], value=1)\nwith ui.row():\n    ui.button('4, 5, 6', on_click=lambda: select.set_options([4, 5, 6], value=4))\n    ui.button('1, 2, 3', on_click=lambda: select.set_options([1, 2, 3], value=1))\n\nui.run()",
    "url": "/documentation/select#update_options"
  },
  {
    "title": "ui.select: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/select#reference"
  },
  {
    "title": "ui.slider: Slider",
    "content": "This element is based on Quasar's `QSlider \u003Chttps://quasar.dev/vue-components/slider\u003E`_ component.\n\n:param min: lower bound of the slider\n:param max: upper bound of the slider\n:param step: step size\n:param value: initial value to set position of the slider\n:param on_change: callback which is invoked when the user releases the slider\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nslider = ui.slider(min=0, max=100, value=50)\nui.label().bind_text_from(slider, 'value')\n\nui.run()",
    "url": "/documentation/slider#slider"
  },
  {
    "title": "ui.slider: Throttle events with leading and trailing options",
    "content": "By default the value change event of a slider is throttled to 0.05 seconds.\nThis means that if you move the slider quickly, the value will only be updated every 0.05 seconds.\n\nBy default both \"leading\" and \"trailing\" events are activated.\nThis means that the very first event is triggered immediately, and the last event is triggered after the throttle time.\n\nThis demo shows how disabling either of these options changes the behavior.\nTo see the effect more clearly, the throttle time is set to 1 second.\nThe first slider shows the default behavior, the second one only sends leading events, and the third only sends trailing events.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.label('default')\nui.slider(min=0, max=10, step=0.1, value=5).props('label-always') \\\n    .on('update:model-value', lambda e: ui.notify(e.args),\n        throttle=1.0)\n\nui.label('leading events only')\nui.slider(min=0, max=10, step=0.1, value=5).props('label-always') \\\n    .on('update:model-value', lambda e: ui.notify(e.args),\n        throttle=1.0, trailing_events=False)\n\nui.label('trailing events only')\nui.slider(min=0, max=10, step=0.1, value=5).props('label-always') \\\n    .on('update:model-value', lambda e: ui.notify(e.args),\n        throttle=1.0, leading_events=False)\n\nui.run()",
    "url": "/documentation/slider#throttle_events_with_leading_and_trailing_options"
  },
  {
    "title": "ui.slider: Disable slider",
    "content": "You can disable a slider with the `disable()` method.\nThis will prevent the user from moving the slider.\nThe slider will also be grayed out.",
    "format": "md",
    "demo": "from nicegui import ui\n\nslider = ui.slider(min=0, max=100, value=50)\nui.button('Disable slider', on_click=slider.disable)\nui.button('Enable slider', on_click=slider.enable)\n\nui.run()",
    "url": "/documentation/slider#disable_slider"
  },
  {
    "title": "ui.slider: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/slider#reference"
  },
  {
    "title": "ui.switch: Switch",
    "content": "This element is based on Quasar's `QToggle \u003Chttps://quasar.dev/vue-components/toggle\u003E`_ component.\n\n:param text: the label to display next to the switch\n:param value: whether it should be active initially (default: `False`)\n:param on_change: callback which is invoked when state is changed by the user\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nswitch = ui.switch('switch me')\nui.label('Switch!').bind_visibility_from(switch, 'value')\n\nui.run()",
    "url": "/documentation/switch#switch"
  },
  {
    "title": "ui.switch: Handle User Interaction",
    "content": "The `on_change` function passed via parameter will be called when the switch is clicked\n*and* when the value changes via `set_value` call.\nTo execute a function only when the user interacts with the switch, you can use the generic `on` method.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.row():\n    s1 = ui.switch(on_change=lambda e: ui.notify(str(e.value)))\n    ui.button('set value', on_click=lambda: s1.set_value(not s1.value))\nwith ui.row():\n    s2 = ui.switch().on('click', lambda e: ui.notify(str(e.sender.value)))\n    ui.button('set value', on_click=lambda: s2.set_value(not s2.value))\n\nui.run()",
    "url": "/documentation/switch#handle_user_interaction"
  },
  {
    "title": "ui.switch: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/switch#reference"
  },
  {
    "title": "ui.textarea: Textarea",
    "content": "This element is based on Quasar's `QInput \u003Chttps://quasar.dev/vue-components/input\u003E`_ component.\nThe ``type`` is set to ``textarea`` to create a multi-line text input.\n\nYou can use the `validation` parameter to define a dictionary of validation rules,\ne.g. ``{'Too long!': lambda value: len(value) \u003C 3}``.\nThe key of the first rule that fails will be displayed as an error message.\nAlternatively, you can pass a callable that returns an optional error message.\nTo disable the automatic validation on every value change, you can use the `without_auto_validation` method.\n\n:param label: displayed name for the textarea\n:param placeholder: text to show if no value is entered\n:param value: the initial value of the field\n:param on_change: callback to execute when the value changes\n:param validation: dictionary of validation rules or a callable that returns an optional error message (default: None for no validation)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.textarea(label='Text', placeholder='start typing',\n            on_change=lambda e: result.set_text('you typed: ' + e.value))\nresult = ui.label()\n\nui.run()",
    "url": "/documentation/textarea#textarea"
  },
  {
    "title": "ui.textarea: Clearable",
    "content": "The `clearable` prop from [Quasar](https://quasar.dev/) adds a button to the input that clears the text.",
    "format": "md",
    "demo": "from nicegui import ui\n\ni = ui.textarea(value='some text').props('clearable')\nui.label().bind_text_from(i, 'value')\n\nui.run()",
    "url": "/documentation/textarea#clearable"
  },
  {
    "title": "ui.textarea: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/textarea#reference"
  },
  {
    "title": "ui.time: Time Input",
    "content": "This element is based on Quasar's `QTime \u003Chttps://quasar.dev/vue-components/time\u003E`_ component.\nThe time is a string in the format defined by the `mask` parameter.\n\n:param value: the initial time\n:param mask: the format of the time string (default: 'HH:mm')\n:param on_change: callback to execute when changing the time\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.time(value='12:00', on_change=lambda e: result.set_text(e.value))\nresult = ui.label()\n\nui.run()",
    "url": "/documentation/time#time_input"
  },
  {
    "title": "ui.time: Input element with time picker",
    "content": "This demo shows how to implement a time picker with an input element.\nWe place an icon in the input element's append slot.\nWhen the icon is clicked, we open a menu with a time picker.\n[QMenu](https://quasar.dev/vue-components/menu)'s \"no-parent-event\" prop is used\nto prevent opening the menu when clicking into the input field.\nAs the menu doesn't come with a \"Close\" button by default, we add one for convenience.\n\nThe time is bound to the input element's value.\nSo both the input element and the time picker will stay in sync whenever the time is changed.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.input('Time') as time:\n    with ui.menu().props('no-parent-event') as menu:\n        with ui.time().bind_value(time):\n            with ui.row().classes('justify-end'):\n                ui.button('Close', on_click=menu.close).props('flat')\n    with time.add_slot('append'):\n        ui.icon('access_time').on('click', menu.open).classes('cursor-pointer')\n\nui.run()",
    "url": "/documentation/time#input_element_with_time_picker"
  },
  {
    "title": "ui.time: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/time#reference"
  },
  {
    "title": "ui.toggle: Toggle",
    "content": "This element is based on Quasar's `QBtnToggle \u003Chttps://quasar.dev/vue-components/button-toggle\u003E`_ component.\n\nThe options can be specified as a list of values, or as a dictionary mapping values to labels.\nAfter manipulating the options, call `update()` to update the options in the UI.\n\n:param options: a list ['value1', ...] or dictionary `{'value1':'label1', ...}` specifying the options\n:param value: the initial value\n:param on_change: callback to execute when selection changes\n:param clearable: whether the toggle can be cleared by clicking the selected option\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\ntoggle1 = ui.toggle([1, 2, 3], value=1)\ntoggle2 = ui.toggle({1: 'A', 2: 'B', 3: 'C'}).bind_value(toggle1, 'value')\n\nui.run()",
    "url": "/documentation/toggle#toggle"
  },
  {
    "title": "ui.toggle: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/toggle#reference"
  },
  {
    "title": "ui.upload: File Upload",
    "content": "Based on Quasar's `QUploader \u003Chttps://quasar.dev/vue-components/uploader\u003E`_ component.\n\nUpload event handlers are called in the following order:\n\n1. ``on_begin_upload``: The client begins uploading one or more files to the server.\n2. ``on_upload``: The upload of an individual file is complete.\n3. ``on_multi_upload``: The upload of all selected files is complete.\n\nThe following event handler is already called during the file selection process:\n\n- ``on_rejected``: One or more files have been rejected.\n\n:param multiple: allow uploading multiple files at once (default: `False`)\n:param max_file_size: maximum file size in bytes (default: `0`)\n:param max_total_size: maximum total size of all files in bytes (default: `0`)\n:param max_files: maximum number of files (default: `0`)\n:param on_begin_upload: callback to execute when upload begins  (*added in version 2.14.0*)\n:param on_upload: callback to execute for each uploaded file\n:param on_multi_upload: callback to execute after multiple files have been uploaded\n:param on_rejected: callback to execute when one or more files have been rejected during file selection\n:param label: label for the uploader (default: `''`)\n:param auto_upload: automatically upload files when they are selected (default: `False`)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.upload(on_upload=lambda e: ui.notify(f'Uploaded {e.name}')).classes('max-w-full')\n\nui.run()",
    "url": "/documentation/upload#file_upload"
  },
  {
    "title": "ui.upload: Upload restrictions",
    "content": "In this demo, the upload is restricted to a maximum file size of 1 MB.\nWhen a file is rejected, a notification is shown.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.upload(on_upload=lambda e: ui.notify(f'Uploaded {e.name}'),\n          on_rejected=lambda: ui.notify('Rejected!'),\n          max_file_size=1_000_000).classes('max-w-full')\n\nui.run()",
    "url": "/documentation/upload#upload_restrictions"
  },
  {
    "title": "ui.upload: Show file content",
    "content": "In this demo, the uploaded markdown file is shown in a dialog.",
    "format": "md",
    "demo": "from nicegui import events, ui\n\nwith ui.dialog().props('full-width') as dialog:\n    with ui.card():\n        content = ui.markdown()\n\ndef handle_upload(e: events.UploadEventArguments):\n    text = e.content.read().decode('utf-8')\n    content.set_content(text)\n    dialog.open()\n\nui.upload(on_upload=handle_upload).props('accept=.md').classes('max-w-full')\n\nui.run()",
    "url": "/documentation/upload#show_file_content"
  },
  {
    "title": "ui.upload: Uploading large files",
    "content": "Large file uploads may encounter issues due to the default file size parameter set within the underlying Starlette library.\nTo ensure smooth uploads of larger files, it is recommended to increase the `spool_max_size` parameter in Starlette's `MultiPartParser` class from the default of `1024 * 1024` (1 MB) to a higher limit that aligns with the expected file sizes.\n\nThis demo increases Starlette Multiparser's `max_file_size` to be kept in RAM to 5 MB.\nThis change allows the system to handle larger files more efficiently by keeping them in RAM, thus avoiding the need to write data to temporary files on disk and preventing upload \"stuttering\".\n\nHowever, be mindful of the potential impact on your server when allowing users to upload large files and retaining them in RAM.",
    "format": "md",
    "demo": "from nicegui import ui\nfrom starlette.formparsers import MultiPartParser\n\nMultiPartParser.spool_max_size = 1024 * 1024 * 5  # 5 MB\n\nui.upload(on_upload=lambda e: ui.notify(f'Uploaded {e.name}')).classes('max-w-full')\n\nui.run()",
    "url": "/documentation/upload#uploading_large_files"
  },
  {
    "title": "ui.upload: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/upload#reference"
  },
  {
    "title": "Controls: Button",
    "content": "This element is based on Quasar's `QBtn \u003Chttps://quasar.dev/vue-components/button\u003E`_ component.\n\nThe ``color`` parameter accepts a Quasar color, a Tailwind color, or a CSS color.\nIf a Quasar color is used, the button will be styled according to the Quasar theme including the color of the text.\nNote that there are colors like \"red\" being both a Quasar color and a CSS color.\nIn such cases the Quasar color will be used.\n\n:param text: the label of the button\n:param on_click: callback which is invoked when button is pressed\n:param color: the color of the button (either a Quasar, Tailwind, or CSS color or `None`, default: 'primary')\n:param icon: the name of an icon to be displayed on the button (default: `None`)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.button('Click me!', on_click=lambda: ui.notify('You clicked me!'))\n\nui.run()",
    "url": "/documentation/section_controls#button"
  },
  {
    "title": "Controls: Button Group",
    "content": "This element is based on Quasar's `QBtnGroup \u003Chttps://quasar.dev/vue-components/button-group\u003E`_ component.\nYou must use the same design props on both the parent button group and the children buttons.\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.button_group():\n    ui.button('One', on_click=lambda: ui.notify('You clicked Button 1!'))\n    ui.button('Two', on_click=lambda: ui.notify('You clicked Button 2!'))\n    ui.button('Three', on_click=lambda: ui.notify('You clicked Button 3!'))\n\nui.run()",
    "url": "/documentation/section_controls#button_group"
  },
  {
    "title": "Controls: Dropdown Button",
    "content": "This element is based on Quasar's `QBtnDropDown \u003Chttps://quasar.dev/vue-components/button-dropdown\u003E`_ component.\n\nThe ``color`` parameter accepts a Quasar color, a Tailwind color, or a CSS color.\nIf a Quasar color is used, the button will be styled according to the Quasar theme including the color of the text.\nNote that there are colors like \"red\" being both a Quasar color and a CSS color.\nIn such cases the Quasar color will be used.\n\n:param text: the label of the button\n:param value: if the dropdown is open or not (default: `False`)\n:param on_value_change: callback which is invoked when the dropdown is opened or closed\n:param on_click: callback which is invoked when button is pressed\n:param color: the color of the button (either a Quasar, Tailwind, or CSS color or `None`, default: 'primary')\n:param icon: the name of an icon to be displayed on the button (default: `None`)\n:param auto_close: whether the dropdown should close automatically when an item is clicked (default: `False`)\n:param split: whether to split the dropdown icon into a separate button (default: `False`)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.dropdown_button('Open me!', auto_close=True):\n    ui.item('Item 1', on_click=lambda: ui.notify('You clicked item 1'))\n    ui.item('Item 2', on_click=lambda: ui.notify('You clicked item 2'))\n\nui.run()",
    "url": "/documentation/section_controls#dropdown_button"
  },
  {
    "title": "Controls: Floating Action Button (FAB)",
    "content": "A floating action button that can be used to trigger an action.\nThis element is based on Quasar's `QFab \u003Chttps://quasar.dev/vue-components/floating-action-button#qfab-api\u003E`_ component.\n\n:param icon: icon to be displayed on the FAB\n:param value: whether the FAB is already opened (default: ``False``)\n:param label: optional label for the FAB\n:param color: background color of the FAB (default: \"primary\")\n:param direction: direction of the FAB (\"up\", \"down\", \"left\", \"right\", default: \"right\")\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.fab('navigation', label='Transport'):\n    ui.fab_action('train', on_click=lambda: ui.notify('Train'))\n    ui.fab_action('sailing', on_click=lambda: ui.notify('Boat'))\n    ui.fab_action('rocket', on_click=lambda: ui.notify('Rocket'))\n\nui.run()",
    "url": "/documentation/section_controls#floating_action_button_(fab)"
  },
  {
    "title": "Controls: Badge",
    "content": "A badge element wrapping Quasar's\n`QBadge \u003Chttps://quasar.dev/vue-components/badge\u003E`_ component.\n\n:param text: the initial value of the text field\n:param color: the color name for component (either a Quasar, Tailwind, or CSS color or `None`, default: \"primary\")\n:param text_color: text color (either a Quasar, Tailwind, or CSS color or `None`, default: `None`)\n:param outline: use 'outline' design (colored text and borders only) (default: False)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.button('Click me!', on_click=lambda: badge.set_text(int(badge.text) + 1)):\n    badge = ui.badge('0', color='red').props('floating')\n\nui.run()",
    "url": "/documentation/section_controls#badge"
  },
  {
    "title": "Controls: Chip",
    "content": "A chip element wrapping Quasar's `QChip \u003Chttps://quasar.dev/vue-components/chip\u003E`_ component.\nIt can be clickable, selectable and removable.\n\n:param text: the initial value of the text field (default: \"\")\n:param icon: the name of an icon to be displayed on the chip (default: `None`)\n:param color: the color name for component (either a Quasar, Tailwind, or CSS color or `None`, default: \"primary\")\n:param text_color: text color (either a Quasar, Tailwind, or CSS color or `None`, default: `None`)\n:param on_click: callback which is invoked when chip is clicked. Makes the chip clickable if set\n:param selectable: whether the chip is selectable (default: `False`)\n:param selected: whether the chip is selected (default: `False`)\n:param on_selection_change: callback which is invoked when the chip's selection state is changed\n:param removable: whether the chip is removable. Shows a small \"x\" button if True (default: `False`)\n:param on_value_change: callback which is invoked when the chip is removed or unremoved\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.row().classes('gap-1'):\n    ui.chip('Click me', icon='ads_click', on_click=lambda: ui.notify('Clicked'))\n    ui.chip('Selectable', selectable=True, icon='bookmark', color='orange')\n    ui.chip('Removable', removable=True, icon='label', color='indigo-3')\n    ui.chip('Styled', icon='star', color='green').props('outline square')\n    ui.chip('Disabled', icon='block', color='red').set_enabled(False)\n\nui.run()",
    "url": "/documentation/section_controls#chip"
  },
  {
    "title": "Controls: Toggle",
    "content": "This element is based on Quasar's `QBtnToggle \u003Chttps://quasar.dev/vue-components/button-toggle\u003E`_ component.\n\nThe options can be specified as a list of values, or as a dictionary mapping values to labels.\nAfter manipulating the options, call `update()` to update the options in the UI.\n\n:param options: a list ['value1', ...] or dictionary `{'value1':'label1', ...}` specifying the options\n:param value: the initial value\n:param on_change: callback to execute when selection changes\n:param clearable: whether the toggle can be cleared by clicking the selected option\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\ntoggle1 = ui.toggle([1, 2, 3], value=1)\ntoggle2 = ui.toggle({1: 'A', 2: 'B', 3: 'C'}).bind_value(toggle1, 'value')\n\nui.run()",
    "url": "/documentation/section_controls#toggle"
  },
  {
    "title": "Controls: Radio Selection",
    "content": "This element is based on Quasar's `QRadio \u003Chttps://quasar.dev/vue-components/radio\u003E`_ component.\n\nThe options can be specified as a list of values, or as a dictionary mapping values to labels.\nAfter manipulating the options, call `update()` to update the options in the UI.\n\n:param options: a list ['value1', ...] or dictionary `{'value1':'label1', ...}` specifying the options\n:param value: the initial value\n:param on_change: callback to execute when selection changes\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nradio1 = ui.radio([1, 2, 3], value=1).props('inline')\nradio2 = ui.radio({1: 'A', 2: 'B', 3: 'C'}).props('inline').bind_value(radio1, 'value')\n\nui.run()",
    "url": "/documentation/section_controls#radio_selection"
  },
  {
    "title": "Controls: Dropdown Selection",
    "content": "This element is based on Quasar's `QSelect \u003Chttps://quasar.dev/vue-components/select\u003E`_ component.\n\nThe options can be specified as a list of values, or as a dictionary mapping values to labels.\nAfter manipulating the options, call `update()` to update the options in the UI.\n\nIf `with_input` is True, an input field is shown to filter the options.\n\nIf `new_value_mode` is not None, it implies `with_input=True` and the user can enter new values in the input field.\nSee `Quasar's documentation \u003Chttps://quasar.dev/vue-components/select#the-new-value-mode-prop\u003E`_ for details.\nNote that this mode is ineffective when setting the `value` property programmatically.\n\nYou can use the `validation` parameter to define a dictionary of validation rules,\ne.g. ``{'Too long!': lambda value: len(value) \u003C 3}``.\nThe key of the first rule that fails will be displayed as an error message.\nAlternatively, you can pass a callable that returns an optional error message.\nTo disable the automatic validation on every value change, you can use the `without_auto_validation` method.\n\n:param options: a list ['value1', ...] or dictionary `{'value1':'label1', ...}` specifying the options\n:param label: the label to display above the selection\n:param value: the initial value\n:param on_change: callback to execute when selection changes\n:param with_input: whether to show an input field to filter the options\n:param new_value_mode: handle new values from user input (default: None, i.e. no new values)\n:param multiple: whether to allow multiple selections\n:param clearable: whether to add a button to clear the selection\n:param validation: dictionary of validation rules or a callable that returns an optional error message (default: None for no validation)\n:param key_generator: a callback or iterator to generate a dictionary key for new values\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nselect1 = ui.select([1, 2, 3], value=1)\nselect2 = ui.select({1: 'One', 2: 'Two', 3: 'Three'}).bind_value(select1, 'value')\n\nui.run()",
    "url": "/documentation/section_controls#dropdown_selection"
  },
  {
    "title": "Controls: Input Chips",
    "content": "An input field that manages a collection of values as visual \"chips\" or tags.\nUsers can type to add new chips and remove existing ones by clicking or using keyboard shortcuts.\n\nThis element is based on Quasar's `QSelect \u003Chttps://quasar.dev/vue-components/select\u003E`_ component.\nUnlike a traditional dropdown selection, this variant focuses on free-form text input with chips,\nmaking it ideal for tags, keywords, or any list of user-defined values.\n\nYou can use the ``validation`` parameter to define a dictionary of validation rules,\ne.g. ``{'Too long!': lambda value: len(value) \u003C 3}``.\nThe key of the first rule that fails will be displayed as an error message.\nAlternatively, you can pass a callable that returns an optional error message.\nTo disable the automatic validation on every value change, you can use the `without_auto_validation` method.\n\n*Added in version 2.22.0*\n\n:param label: the label to display above the selection\n:param value: the initial value\n:param on_change: callback to execute when selection changes\n:param new_value_mode: handle new values from user input (default: \"toggle\")\n:param clearable: whether to add a button to clear the selection\n:param validation: dictionary of validation rules or a callable that returns an optional error message (default: None for no validation)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.input_chips('My favorite chips', value=['Pringles', 'Doritos', \"Lay's\"])\n\nui.run()",
    "url": "/documentation/section_controls#input_chips"
  },
  {
    "title": "Controls: Checkbox",
    "content": "This element is based on Quasar's `QCheckbox \u003Chttps://quasar.dev/vue-components/checkbox\u003E`_ component.\n\n:param text: the label to display next to the checkbox\n:param value: whether it should be checked initially (default: `False`)\n:param on_change: callback to execute when value changes\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\ncheckbox = ui.checkbox('check me')\nui.label('Check!').bind_visibility_from(checkbox, 'value')\n\nui.run()",
    "url": "/documentation/section_controls#checkbox"
  },
  {
    "title": "Controls: Switch",
    "content": "This element is based on Quasar's `QToggle \u003Chttps://quasar.dev/vue-components/toggle\u003E`_ component.\n\n:param text: the label to display next to the switch\n:param value: whether it should be active initially (default: `False`)\n:param on_change: callback which is invoked when state is changed by the user\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nswitch = ui.switch('switch me')\nui.label('Switch!').bind_visibility_from(switch, 'value')\n\nui.run()",
    "url": "/documentation/section_controls#switch"
  },
  {
    "title": "Controls: Slider",
    "content": "This element is based on Quasar's `QSlider \u003Chttps://quasar.dev/vue-components/slider\u003E`_ component.\n\n:param min: lower bound of the slider\n:param max: upper bound of the slider\n:param step: step size\n:param value: initial value to set position of the slider\n:param on_change: callback which is invoked when the user releases the slider\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nslider = ui.slider(min=0, max=100, value=50)\nui.label().bind_text_from(slider, 'value')\n\nui.run()",
    "url": "/documentation/section_controls#slider"
  },
  {
    "title": "Controls: Range",
    "content": "This element is based on Quasar's `QRange \u003Chttps://quasar.dev/vue-components/range\u003E`_ component.\n\n:param min: lower bound of the range\n:param max: upper bound of the range\n:param step: step size\n:param value: initial value to set min and max position of the range\n:param on_change: callback which is invoked when the user releases the range\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nmin_max_range = ui.range(min=0, max=100, value={'min': 20, 'max': 80})\nui.label().bind_text_from(min_max_range, 'value',\n                          backward=lambda v: f'min: {v[\"min\"]}, max: {v[\"max\"]}')\n\nui.run()",
    "url": "/documentation/section_controls#range"
  },
  {
    "title": "Controls: Rating",
    "content": "This element is based on Quasar's `QRating \u003Chttps://quasar.dev/vue-components/rating\u003E`_ component.\n\n*Added in version 2.12.0*\n\n:param value: initial value (default: ``None``)\n:param max: maximum rating, number of icons (default: 5)\n:param icon: name of icons to be displayed (default: star)\n:param icon_selected: name of an icon to be displayed when selected (default: same as ``icon``)\n:param icon_half: name of an icon to be displayed when half-selected (default: same as ``icon``)\n:param color: color(s) of the icons (Quasar, Tailwind, or CSS colors or ``None``, default: \"primary\")\n:param size: size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl), examples: 16px, 2rem\n:param on_change: callback to execute when selection changes\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.rating(value=4)\n\nui.run()",
    "url": "/documentation/section_controls#rating"
  },
  {
    "title": "Controls: Joystick",
    "content": "Create a joystick based on `nipple.js \u003Chttps://yoannmoi.net/nipplejs/\u003E`_.\n\n:param on_start: callback for when the user touches the joystick\n:param on_move: callback for when the user moves the joystick\n:param on_end: callback for when the user releases the joystick\n:param throttle: throttle interval in seconds for the move event (default: 0.05)\n:param options: arguments like `color` which should be passed to the `underlying nipple.js library \u003Chttps://github.com/yoannmoinet/nipplejs#options\u003E`_\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.joystick(\n    color='blue', size=50,\n    on_move=lambda e: coordinates.set_text(f'{e.x:.3f}, {e.y:.3f}'),\n    on_end=lambda _: coordinates.set_text('0, 0'),\n).classes('bg-slate-300')\ncoordinates = ui.label('0, 0')\n\nui.run()",
    "url": "/documentation/section_controls#joystick"
  },
  {
    "title": "Controls: Text Input",
    "content": "This element is based on Quasar's `QInput \u003Chttps://quasar.dev/vue-components/input\u003E`_ component.\n\nThe `on_change` event is called on every keystroke and the value updates accordingly.\nIf you want to wait until the user confirms the input, you can register a custom event callback, e.g.\n`ui.input(...).on('keydown.enter', ...)` or `ui.input(...).on('blur', ...)`.\n\nYou can use the `validation` parameter to define a dictionary of validation rules,\ne.g. ``{'Too long!': lambda value: len(value) \u003C 3}``.\nThe key of the first rule that fails will be displayed as an error message.\nAlternatively, you can pass a callable that returns an optional error message.\nTo disable the automatic validation on every value change, you can use the `without_auto_validation` method.\n\nNote about styling the input:\nQuasar's `QInput` component is a wrapper around a native `input` element.\nThis means that you cannot style the input directly,\nbut you can use the `input-class` and `input-style` props to style the native input element.\nSee the \"Style\" props section on the `QInput \u003Chttps://quasar.dev/vue-components/input\u003E`_ documentation for more details.\n\n:param label: displayed label for the text input\n:param placeholder: text to show if no value is entered\n:param value: the current value of the text input\n:param password: whether to hide the input (default: False)\n:param password_toggle_button: whether to show a button to toggle the password visibility (default: False)\n:param on_change: callback to execute when the value changes\n:param autocomplete: optional list of strings for autocompletion\n:param validation: dictionary of validation rules or a callable that returns an optional error message (default: None for no validation)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.input(label='Text', placeholder='start typing',\n         on_change=lambda e: result.set_text('you typed: ' + e.value),\n         validation={'Input too long': lambda value: len(value) \u003C 20})\nresult = ui.label()\n\nui.run()",
    "url": "/documentation/section_controls#text_input"
  },
  {
    "title": "Controls: Textarea",
    "content": "This element is based on Quasar's `QInput \u003Chttps://quasar.dev/vue-components/input\u003E`_ component.\nThe ``type`` is set to ``textarea`` to create a multi-line text input.\n\nYou can use the `validation` parameter to define a dictionary of validation rules,\ne.g. ``{'Too long!': lambda value: len(value) \u003C 3}``.\nThe key of the first rule that fails will be displayed as an error message.\nAlternatively, you can pass a callable that returns an optional error message.\nTo disable the automatic validation on every value change, you can use the `without_auto_validation` method.\n\n:param label: displayed name for the textarea\n:param placeholder: text to show if no value is entered\n:param value: the initial value of the field\n:param on_change: callback to execute when the value changes\n:param validation: dictionary of validation rules or a callable that returns an optional error message (default: None for no validation)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.textarea(label='Text', placeholder='start typing',\n            on_change=lambda e: result.set_text('you typed: ' + e.value))\nresult = ui.label()\n\nui.run()",
    "url": "/documentation/section_controls#textarea"
  },
  {
    "title": "Controls: CodeMirror",
    "content": "An element to create a code editor using `CodeMirror \u003Chttps://codemirror.net/\u003E`_.\n\nIt supports syntax highlighting for over 140 languages, more than 30 themes, line numbers, code folding, (limited) auto-completion, and more.\n\nSupported languages and themes:\n    - Languages: A list of supported languages can be found in the `@codemirror/language-data \u003Chttps://github.com/codemirror/language-data/blob/main/src/language-data.ts\u003E`_ package.\n    - Themes: A list can be found in the `@uiw/codemirror-themes-all \u003Chttps://github.com/uiwjs/react-codemirror/tree/master/themes/all\u003E`_ package.\n\nAt runtime, the methods `supported_languages` and `supported_themes` can be used to get supported languages and themes.\n\n:param value: initial value of the editor (default: \"\")\n:param on_change: callback to be executed when the value changes (default: `None`)\n:param language: initial language of the editor (case-insensitive, default: `None`)\n:param theme: initial theme of the editor (default: \"basicLight\")\n:param indent: string to use for indentation (any string consisting entirely of the same whitespace character, default: \"    \")\n:param line_wrapping: whether to wrap lines (default: `False`)\n:param highlight_whitespace: whether to highlight whitespace (default: `False`)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\neditor = ui.codemirror('print(\"Edit me!\")', language='Python').classes('h-32')\nui.select(editor.supported_languages, label='Language', clearable=True) \\\n    .classes('w-32').bind_value(editor, 'language')\nui.select(editor.supported_themes, label='Theme') \\\n    .classes('w-32').bind_value(editor, 'theme')\n\nui.run()",
    "url": "/documentation/section_controls#codemirror"
  },
  {
    "title": "Controls: Number Input",
    "content": "This element is based on Quasar's `QInput \u003Chttps://quasar.dev/vue-components/input\u003E`_ component.\n\nYou can use the `validation` parameter to define a dictionary of validation rules,\ne.g. ``{'Too small!': lambda value: value \u003E 3}``.\nThe key of the first rule that fails will be displayed as an error message.\nAlternatively, you can pass a callable that returns an optional error message.\nTo disable the automatic validation on every value change, you can use the `without_auto_validation` method.\n\n:param label: displayed name for the number input\n:param placeholder: text to show if no value is entered\n:param value: the initial value of the field\n:param min: the minimum value allowed\n:param max: the maximum value allowed\n:param precision: the number of decimal places allowed (default: no limit, negative: decimal places before the dot)\n:param step: the step size for the stepper buttons\n:param prefix: a prefix to prepend to the displayed value\n:param suffix: a suffix to append to the displayed value\n:param format: a string like \"%.2f\" to format the displayed value\n:param on_change: callback to execute when the value changes\n:param validation: dictionary of validation rules or a callable that returns an optional error message (default: None for no validation)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.number(label='Number', value=3.1415927, format='%.2f',\n          on_change=lambda e: result.set_text(f'you entered: {e.value}'))\nresult = ui.label()\n\nui.run()",
    "url": "/documentation/section_controls#number_input"
  },
  {
    "title": "Controls: Knob",
    "content": "This element is based on Quasar's `QKnob \u003Chttps://quasar.dev/vue-components/knob\u003E`_ component.\nThe element is used to take a number input from the user through mouse/touch panning.\n\n:param value: the initial value (default: 0.0)\n:param min: the minimum value (default: 0.0)\n:param max: the maximum value (default: 1.0)\n:param step: the step size (default: 0.01)\n:param color: knob color (either a Quasar, Tailwind, or CSS color or `None`, default: \"primary\")\n:param center_color: color name for the center part of the component, examples: primary, teal-10\n:param track_color: color name for the track of the component, examples: primary, teal-10\n:param size: size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl), examples: 16px, 2rem\n:param show_value: whether to show the value as text\n:param on_change: callback to execute when the value changes\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nknob = ui.knob(0.3, show_value=True)\n\nwith ui.knob(color='orange', track_color='grey-2').bind_value(knob, 'value'):\n    ui.icon('volume_up')\n\nui.run()",
    "url": "/documentation/section_controls#knob"
  },
  {
    "title": "Controls: Color Input",
    "content": "This element extends Quasar's `QInput \u003Chttps://quasar.dev/vue-components/input\u003E`_ component with a color picker.\n\n:param label: displayed label for the color input\n:param placeholder: text to show if no color is selected\n:param value: the current color value\n:param on_change: callback to execute when the value changes\n:param preview: change button background to selected color (default: False)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nlabel = ui.label('Change my color!')\nui.color_input(label='Color', value='#000000',\n               on_change=lambda e: label.style(f'color:{e.value}'))\n\nui.run()",
    "url": "/documentation/section_controls#color_input"
  },
  {
    "title": "Controls: Color Picker",
    "content": "This element is based on Quasar's `QMenu \u003Chttps://quasar.dev/vue-components/menu\u003E`_ and\n`QColor \u003Chttps://quasar.dev/vue-components/color-picker\u003E`_ components.\n\n:param on_pick: callback to execute when a color is picked\n:param value: whether the menu is already opened (default: `False`)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.button(icon='colorize') as button:\n    ui.color_picker(on_pick=lambda e: button.classes(f'!bg-[{e.color}]'))\n\nui.run()",
    "url": "/documentation/section_controls#color_picker"
  },
  {
    "title": "Controls: Date Input",
    "content": "This element is based on Quasar's `QDate \u003Chttps://quasar.dev/vue-components/date\u003E`_ component.\nThe date is a string in the format defined by the `mask` parameter.\n\nYou can also use the `range` or `multiple` props to select a range of dates or multiple dates::\n\n    ui.date({'from': '2023-01-01', 'to': '2023-01-05'}).props('range')\n    ui.date(['2023-01-01', '2023-01-02', '2023-01-03']).props('multiple')\n    ui.date([{'from': '2023-01-01', 'to': '2023-01-05'}, '2023-01-07']).props('multiple range')\n\n:param value: the initial date\n:param mask: the format of the date string (default: 'YYYY-MM-DD')\n:param on_change: callback to execute when changing the date\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.date(value='2023-01-01', on_change=lambda e: result.set_text(e.value))\nresult = ui.label()\n\nui.run()",
    "url": "/documentation/section_controls#date_input"
  },
  {
    "title": "Controls: Time Input",
    "content": "This element is based on Quasar's `QTime \u003Chttps://quasar.dev/vue-components/time\u003E`_ component.\nThe time is a string in the format defined by the `mask` parameter.\n\n:param value: the initial time\n:param mask: the format of the time string (default: 'HH:mm')\n:param on_change: callback to execute when changing the time\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.time(value='12:00', on_change=lambda e: result.set_text(e.value))\nresult = ui.label()\n\nui.run()",
    "url": "/documentation/section_controls#time_input"
  },
  {
    "title": "Controls: File Upload",
    "content": "Based on Quasar's `QUploader \u003Chttps://quasar.dev/vue-components/uploader\u003E`_ component.\n\nUpload event handlers are called in the following order:\n\n1. ``on_begin_upload``: The client begins uploading one or more files to the server.\n2. ``on_upload``: The upload of an individual file is complete.\n3. ``on_multi_upload``: The upload of all selected files is complete.\n\nThe following event handler is already called during the file selection process:\n\n- ``on_rejected``: One or more files have been rejected.\n\n:param multiple: allow uploading multiple files at once (default: `False`)\n:param max_file_size: maximum file size in bytes (default: `0`)\n:param max_total_size: maximum total size of all files in bytes (default: `0`)\n:param max_files: maximum number of files (default: `0`)\n:param on_begin_upload: callback to execute when upload begins  (*added in version 2.14.0*)\n:param on_upload: callback to execute for each uploaded file\n:param on_multi_upload: callback to execute after multiple files have been uploaded\n:param on_rejected: callback to execute when one or more files have been rejected during file selection\n:param label: label for the uploader (default: `''`)\n:param auto_upload: automatically upload files when they are selected (default: `False`)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.upload(on_upload=lambda e: ui.notify(f'Uploaded {e.name}')).classes('max-w-full')\n\nui.run()",
    "url": "/documentation/section_controls#file_upload"
  },
  {
    "title": "ui.aggrid: AG Grid",
    "content": "An element to create a grid using `AG Grid \u003Chttps://www.ag-grid.com/\u003E`_.\n\nThe methods ``run_grid_method`` and ``run_row_method`` can be used to interact with the AG Grid instance on the client.\n\n:param options: dictionary of AG Grid options\n:param html_columns: list of columns that should be rendered as HTML (default: ``[]``)\n:param theme: AG Grid theme (default: \"balham\")\n:param auto_size_columns: whether to automatically resize columns to fit the grid width (default: ``True``)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\ngrid = ui.aggrid({\n    'defaultColDef': {'flex': 1},\n    'columnDefs': [\n        {'headerName': 'Name', 'field': 'name'},\n        {'headerName': 'Age', 'field': 'age'},\n        {'headerName': 'Parent', 'field': 'parent', 'hide': True},\n    ],\n    'rowData': [\n        {'name': 'Alice', 'age': 18, 'parent': 'David'},\n        {'name': 'Bob', 'age': 21, 'parent': 'Eve'},\n        {'name': 'Carol', 'age': 42, 'parent': 'Frank'},\n    ],\n    'rowSelection': 'multiple',\n}).classes('max-h-40')\n\ndef update():\n    grid.options['rowData'][0]['age'] += 1\n    grid.update()\n\nui.button('Update', on_click=update)\nui.button('Select all', on_click=lambda: grid.run_grid_method('selectAll'))\nui.button('Show parent', on_click=lambda: grid.run_grid_method('setColumnsVisible', ['parent'], True))\n\nui.run()",
    "url": "/documentation/aggrid#ag_grid"
  },
  {
    "title": "ui.aggrid: Select AG Grid Rows",
    "content": "You can add checkboxes to grid cells to allow the user to select single or multiple rows.\n\nTo retrieve the currently selected rows, use the `get_selected_rows` method.\nThis method returns a list of rows as dictionaries.\n\nIf `rowSelection` is set to `'single'` or to get the first selected row,\nyou can also use the `get_selected_row` method.\nThis method returns a single row as a dictionary or `None` if no row is selected.\n\nSee the [AG Grid documentation](https://www.ag-grid.com/javascript-data-grid/row-selection/#example-single-row-selection) for more information.",
    "format": "md",
    "demo": "from nicegui import ui\n\n@ui.page('/')\ndef page():\n    grid = ui.aggrid({\n        'columnDefs': [\n            {'headerName': 'Name', 'field': 'name', 'checkboxSelection': True},\n            {'headerName': 'Age', 'field': 'age'},\n        ],\n        'rowData': [\n            {'name': 'Alice', 'age': 18},\n            {'name': 'Bob', 'age': 21},\n            {'name': 'Carol', 'age': 42},\n        ],\n        'rowSelection': 'multiple',\n    }).classes('max-h-40')\n\n    async def output_selected_rows():\n        rows = await grid.get_selected_rows()\n        if rows:\n            for row in rows:\n                ui.notify(f\"{row['name']}, {row['age']}\")\n        else:\n            ui.notify('No rows selected.')\n\n    async def output_selected_row():\n        row = await grid.get_selected_row()\n        if row:\n            ui.notify(f\"{row['name']}, {row['age']}\")\n        else:\n            ui.notify('No row selected!')\n\n    ui.button('Output selected rows', on_click=output_selected_rows)\n    ui.button('Output selected row', on_click=output_selected_row)\n\nui.run()",
    "url": "/documentation/aggrid#select_ag_grid_rows"
  },
  {
    "title": "ui.aggrid: Filter Rows using Mini Filters",
    "content": "You can add [mini filters](https://ag-grid.com/javascript-data-grid/filter-set-mini-filter/)\nto the header of each column to filter the rows.\n\nNote how the \"agTextColumnFilter\" matches individual characters, like \"a\" in \"Alice\" and \"Carol\",\nwhile the \"agNumberColumnFilter\" matches the entire number, like \"18\" and \"21\", but not \"1\".",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.aggrid({\n    'columnDefs': [\n        {'headerName': 'Name', 'field': 'name', 'filter': 'agTextColumnFilter', 'floatingFilter': True},\n        {'headerName': 'Age', 'field': 'age', 'filter': 'agNumberColumnFilter', 'floatingFilter': True},\n    ],\n    'rowData': [\n        {'name': 'Alice', 'age': 18},\n        {'name': 'Bob', 'age': 21},\n        {'name': 'Carol', 'age': 42},\n    ],\n}).classes('max-h-40')\n\nui.run()",
    "url": "/documentation/aggrid#filter_rows_using_mini_filters"
  },
  {
    "title": "ui.aggrid: AG Grid with Conditional Cell Formatting",
    "content": "This demo shows how to use [cellClassRules](https://www.ag-grid.com/javascript-grid-cell-styles/#cell-class-rules)\nto conditionally format cells based on their values.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.aggrid({\n    'columnDefs': [\n        {'headerName': 'Name', 'field': 'name'},\n        {'headerName': 'Age', 'field': 'age', 'cellClassRules': {\n            'bg-red-300': 'x \u003C 21',\n            'bg-green-300': 'x \u003E= 21',\n        }},\n    ],\n    'rowData': [\n        {'name': 'Alice', 'age': 18},\n        {'name': 'Bob', 'age': 21},\n        {'name': 'Carol', 'age': 42},\n    ],\n})\n\nui.run()",
    "url": "/documentation/aggrid#ag_grid_with_conditional_cell_formatting"
  },
  {
    "title": "ui.aggrid: Create Grid from Pandas DataFrame",
    "content": "You can create an AG Grid from a Pandas DataFrame using the `from_pandas` method.\nThis method takes a Pandas DataFrame as input and returns an AG Grid.",
    "format": "md",
    "demo": "import pandas as pd\nfrom nicegui import ui\n\ndf = pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})\nui.aggrid.from_pandas(df).classes('max-h-40')\n\nui.run()",
    "url": "/documentation/aggrid#create_grid_from_pandas_dataframe"
  },
  {
    "title": "ui.aggrid: Create Grid from Polars DataFrame",
    "content": "You can create an AG Grid from a Polars DataFrame using the `from_polars` method.\nThis method takes a Polars DataFrame as input and returns an AG Grid.\n\n*Added in version 2.7.0*",
    "format": "md",
    "demo": "import polars as pl\nfrom nicegui import ui\n\ndf = pl.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})\nui.aggrid.from_polars(df).classes('max-h-40')\n\nui.run()",
    "url": "/documentation/aggrid#create_grid_from_polars_dataframe"
  },
  {
    "title": "ui.aggrid: Render columns as HTML",
    "content": "You can render columns as HTML by passing a list of column indices to the `html_columns` argument.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.aggrid({\n    'columnDefs': [\n        {'headerName': 'Name', 'field': 'name'},\n        {'headerName': 'URL', 'field': 'url'},\n    ],\n    'rowData': [\n        {'name': 'Google', 'url': '\u003Ca href=\"https://google.com\"\u003Ehttps://google.com\u003C/a\u003E'},\n        {'name': 'Facebook', 'url': '\u003Ca href=\"https://facebook.com\"\u003Ehttps://facebook.com\u003C/a\u003E'},\n    ],\n}, html_columns=[1])\n\nui.run()",
    "url": "/documentation/aggrid#render_columns_as_html"
  },
  {
    "title": "ui.aggrid: Respond to an AG Grid event",
    "content": "All AG Grid events are passed through to NiceGUI via the AG Grid global listener.\nThese events can be subscribed to using the `.on()` method.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.aggrid({\n    'columnDefs': [\n        {'headerName': 'Name', 'field': 'name'},\n        {'headerName': 'Age', 'field': 'age'},\n    ],\n    'rowData': [\n        {'name': 'Alice', 'age': 18},\n        {'name': 'Bob', 'age': 21},\n        {'name': 'Carol', 'age': 42},\n    ],\n}).on('cellClicked', lambda event: ui.notify(f'Cell value: {event.args[\"value\"]}'))\n\nui.run()",
    "url": "/documentation/aggrid#respond_to_an_ag_grid_event"
  },
  {
    "title": "ui.aggrid: AG Grid with complex objects",
    "content": "You can use nested complex objects in AG Grid by separating the field names with a period.\n(This is the reason why keys in `rowData` are not allowed to contain periods.)",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.aggrid({\n    'columnDefs': [\n        {'headerName': 'First name', 'field': 'name.first'},\n        {'headerName': 'Last name', 'field': 'name.last'},\n        {'headerName': 'Age', 'field': 'age'}\n    ],\n    'rowData': [\n        {'name': {'first': 'Alice', 'last': 'Adams'}, 'age': 18},\n        {'name': {'first': 'Bob', 'last': 'Brown'}, 'age': 21},\n        {'name': {'first': 'Carol', 'last': 'Clark'}, 'age': 42},\n    ],\n}).classes('max-h-40')\n\nui.run()",
    "url": "/documentation/aggrid#ag_grid_with_complex_objects"
  },
  {
    "title": "ui.aggrid: AG Grid with dynamic row height",
    "content": "You can set the height of individual rows by passing a function to the `getRowHeight` argument.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.aggrid({\n    'columnDefs': [{'field': 'name'}, {'field': 'age'}],\n    'rowData': [\n        {'name': 'Alice', 'age': '18'},\n        {'name': 'Bob', 'age': '21'},\n        {'name': 'Carol', 'age': '42'},\n    ],\n    ':getRowHeight': 'params =\u003E params.data.age \u003E 35 ? 50 : 25',\n}).classes('max-h-40')\n\nui.run()",
    "url": "/documentation/aggrid#ag_grid_with_dynamic_row_height"
  },
  {
    "title": "ui.aggrid: Run row methods",
    "content": "You can run methods on individual rows by using the `run_row_method` method.\nThis method takes the row ID, the method name and the method arguments as arguments.\nThe row ID is either the row index (as a string) or the value of the `getRowId` function.\n\nThe following demo shows how to use it to update cell values.\nNote that the row selection is preserved when the value is updated.\nThis would not be the case if the grid was updated using the `update` method.",
    "format": "md",
    "demo": "from nicegui import ui\n\ngrid = ui.aggrid({\n    'columnDefs': [\n        {'field': 'name', 'checkboxSelection': True},\n        {'field': 'age'},\n    ],\n    'rowData': [\n        {'name': 'Alice', 'age': 18},\n        {'name': 'Bob', 'age': 21},\n        {'name': 'Carol', 'age': 42},\n    ],\n    ':getRowId': '(params) =\u003E params.data.name',\n})\nui.button('Update',\n          on_click=lambda: grid.run_row_method('Alice', 'setDataValue', 'age', 99))\n\nui.run()",
    "url": "/documentation/aggrid#run_row_methods"
  },
  {
    "title": "ui.aggrid: Filter return values",
    "content": "You can filter the return values of method calls by passing string that defines a JavaScript function.\nThis demo runs the grid method \"getDisplayedRowAtIndex\" and returns the \"data\" property of the result.\n\nNote that requesting data from the client is only supported for page functions, not for the shared auto-index page.",
    "format": "md",
    "demo": "from nicegui import ui\n\n@ui.page('/')\ndef page():\n    grid = ui.aggrid({\n        'columnDefs': [{'field': 'name'}],\n        'rowData': [{'name': 'Alice'}, {'name': 'Bob'}],\n    })\n\n    async def get_first_name() -\u003E None:\n        row = await grid.run_grid_method('g =\u003E g.getDisplayedRowAtIndex(0).data')\n        ui.notify(row['name'])\n\n    ui.button('Get First Name', on_click=get_first_name)\n\nui.run()",
    "url": "/documentation/aggrid#filter_return_values"
  },
  {
    "title": "ui.aggrid: Handle theme change",
    "content": "You can change the theme of the AG Grid by adding or removing classes.\nThis demo shows how to change the theme using a switch.",
    "format": "md",
    "demo": "from nicegui import events, ui\n\ngrid = ui.aggrid({})\n\ndef handle_theme_change(e: events.ValueChangeEventArguments):\n    grid.classes(add='ag-theme-balham-dark' if e.value else 'ag-theme-balham',\n                 remove='ag-theme-balham ag-theme-balham-dark')\n\nui.switch('Dark', on_change=handle_theme_change)\n\nui.run()",
    "url": "/documentation/aggrid#handle_theme_change"
  },
  {
    "title": "ui.aggrid: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/aggrid#reference"
  },
  {
    "title": "ui.circular_progress: Circular Progress",
    "content": "A circular progress bar wrapping Quasar's\n`QCircularProgress \u003Chttps://quasar.dev/vue-components/circular-progress\u003E`_.\n\n:param value: the initial value of the field\n:param min: the minimum value (default: 0.0)\n:param max: the maximum value (default: 1.0)\n:param size: the size of the progress circle (default: \"xl\")\n:param show_value: whether to show a value label in the center (default: `True`)\n:param color: color (either a Quasar, Tailwind, or CSS color or `None`, default: \"primary\")\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nslider = ui.slider(min=0, max=1, step=0.01, value=0.5)\nui.circular_progress().bind_value_from(slider, 'value')\n\nui.run()",
    "url": "/documentation/circular_progress#circular_progress"
  },
  {
    "title": "ui.circular_progress: Nested Elements",
    "content": "You can put any element like icon, button etc inside a circular progress using the `with` statement.\nJust make sure it fits the bounds and disable the default behavior of showing the value.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.row().classes('items-center m-auto'):\n    with ui.circular_progress(value=0.1, show_value=False) as progress:\n        ui.button(\n            icon='star',\n            on_click=lambda: progress.set_value(progress.value + 0.1)\n        ).props('flat round')\n    ui.label('click to increase progress')\n\nui.run()",
    "url": "/documentation/circular_progress#nested_elements"
  },
  {
    "title": "ui.circular_progress: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/circular_progress#reference"
  },
  {
    "title": "ui.code: Code",
    "content": "This element displays a code block with syntax highlighting.\n\nIn secure environments (HTTPS or localhost), a copy button is displayed to copy the code to the clipboard.\n\n:param content: code to display\n:param language: language of the code (default: \"python\")\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.code('''\n    from nicegui import ui\n\n    ui.label('Code inception!')\n\n    ui.run()\n''').classes('w-full')\n\nui.run()",
    "url": "/documentation/code#code"
  },
  {
    "title": "ui.code: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/code#reference"
  },
  {
    "title": "ui.echart: Apache EChart",
    "content": "An element to create a chart using `ECharts \u003Chttps://echarts.apache.org/\u003E`_.\nUpdates can be pushed to the chart by changing the `options` property.\nAfter data has changed, call the `update` method to refresh the chart.\n\n:param options: dictionary of EChart options\n:param on_click_point: callback that is invoked when a point is clicked\n:param enable_3d: enforce importing the echarts-gl library\n:param renderer: renderer to use (\"canvas\" or \"svg\", *added in version 2.7.0*)\n:param theme: an EChart theme configuration (dictionary or a URL returning a JSON object, *added in version 2.15.0*)\n",
    "format": "rst",
    "demo": "from nicegui import ui\nfrom random import random\n\nechart = ui.echart({\n    'xAxis': {'type': 'value'},\n    'yAxis': {'type': 'category', 'data': ['A', 'B'], 'inverse': True},\n    'legend': {'textStyle': {'color': 'gray'}},\n    'series': [\n        {'type': 'bar', 'name': 'Alpha', 'data': [0.1, 0.2]},\n        {'type': 'bar', 'name': 'Beta', 'data': [0.3, 0.4]},\n    ],\n})\n\ndef update():\n    echart.options['series'][0]['data'][0] = random()\n    echart.update()\n\nui.button('Update', on_click=update)\n\nui.run()",
    "url": "/documentation/echart#apache_echart"
  },
  {
    "title": "ui.echart: EChart with clickable points",
    "content": "You can register a callback for an event when a series point is clicked.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.echart({\n    'xAxis': {'type': 'category'},\n    'yAxis': {'type': 'value'},\n    'series': [{'type': 'line', 'data': [20, 10, 30, 50, 40, 30]}],\n}, on_point_click=ui.notify)\n\nui.run()",
    "url": "/documentation/echart#echart_with_clickable_points"
  },
  {
    "title": "ui.echart: EChart with dynamic properties",
    "content": "Dynamic properties can be passed to chart elements to customize them such as apply an axis label format.\nTo make a property dynamic, prefix a colon \":\" to the property name.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.echart({\n    'xAxis': {'type': 'category'},\n    'yAxis': {'axisLabel': {':formatter': 'value =\u003E \"$\" + value'}},\n    'series': [{'type': 'line', 'data': [5, 8, 13, 21, 34, 55]}],\n})\n\nui.run()",
    "url": "/documentation/echart#echart_with_dynamic_properties"
  },
  {
    "title": "ui.echart: EChart with custom theme",
    "content": "You can apply custom themes created with the [Theme Builder](https://echarts.apache.org/en/theme-builder.html).\n\nInstead of passing the theme as a dictionary, you can pass a URL to a JSON file.\nThis allows the browser to cache the theme and load it faster when the same theme is used multiple times.\n\n*Added in version 2.15.0*",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.echart({\n    'xAxis': {'type': 'category'},\n    'yAxis': {'type': 'value'},\n    'series': [{'type': 'bar', 'data': [20, 10, 30, 50, 40, 30]}],\n}, theme={\n    'color': ['#b687ac', '#28738a', '#a78f8f'],\n    'backgroundColor': 'rgba(254,248,239,1)',\n})\n\nui.run()",
    "url": "/documentation/echart#echart_with_custom_theme"
  },
  {
    "title": "ui.echart: EChart from pyecharts",
    "content": "You can create an EChart element from a pyecharts object using the `from_pyecharts` method.\nFor defining dynamic options like a formatter function, you can use the `JsCode` class from `pyecharts.commons.utils`.\nAlternatively, you can use a colon \":\" to prefix the property name to indicate that the value is a JavaScript expression.",
    "format": "md",
    "demo": "from nicegui import ui\nfrom pyecharts.charts import Bar\nfrom pyecharts.commons.utils import JsCode\nfrom pyecharts.options import AxisOpts\n\nui.echart.from_pyecharts(\n    Bar()\n    .add_xaxis(['A', 'B', 'C'])\n    .add_yaxis('ratio', [1, 2, 4])\n    .set_global_opts(\n        xaxis_opts=AxisOpts(axislabel_opts={\n            ':formatter': r'(val, idx) =\u003E `group ${val}`',\n        }),\n        yaxis_opts=AxisOpts(axislabel_opts={\n            'formatter': JsCode(r'(val, idx) =\u003E `${val}%`'),\n        }),\n    )\n)\n\nui.run()",
    "url": "/documentation/echart#echart_from_pyecharts"
  },
  {
    "title": "ui.echart: Run methods",
    "content": "You can run methods of the EChart instance using the `run_chart_method` method.\nThis demo shows how to show and hide the loading animation, how to get the current width of the chart,\nand how to add tooltips with a custom formatter.\n\nThe colon \":\" in front of the method name \"setOption\" indicates that the argument is a JavaScript expression\nthat is evaluated on the client before it is passed to the method.\n\nNote that requesting data from the client is only supported for page functions, not for the shared auto-index page.",
    "format": "md",
    "demo": "from nicegui import ui\n\n@ui.page('/')\ndef page():\n    echart = ui.echart({\n        'xAxis': {'type': 'category', 'data': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']},\n        'yAxis': {'type': 'value'},\n        'series': [{'type': 'line', 'data': [150, 230, 224, 218, 135]}],\n    })\n\n    ui.button('Show Loading', on_click=lambda: echart.run_chart_method('showLoading'))\n    ui.button('Hide Loading', on_click=lambda: echart.run_chart_method('hideLoading'))\n\n    async def get_width():\n        width = await echart.run_chart_method('getWidth')\n        ui.notify(f'Width: {width}')\n    ui.button('Get Width', on_click=get_width)\n\n    ui.button('Set Tooltip', on_click=lambda: echart.run_chart_method(\n        ':setOption', r'{tooltip: {formatter: params =\u003E \"$\" + params.value}}',\n    ))\n\nui.run()",
    "url": "/documentation/echart#run_methods"
  },
  {
    "title": "ui.echart: Arbitrary chart events",
    "content": "You can register arbitrary event listeners for the chart using the `on` method and a \"chart:\" prefix.\nThis demo shows how to register a callback for the \"selectchanged\" event which is triggered when the user selects a point.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.echart({\n    'toolbox': {'feature': {'brush': {'type': ['rect']}}},\n    'brush': {},\n    'xAxis': {'type': 'category'},\n    'yAxis': {'type': 'value'},\n    'series': [{'type': 'line', 'data': [1, 2, 3]}],\n}).on('chart:selectchanged', lambda e: label.set_text(\n    f'Selected point {e.args[\"fromActionPayload\"][\"dataIndexInside\"]}'\n))\nlabel = ui.label()\n\nui.run()",
    "url": "/documentation/echart#arbitrary_chart_events"
  },
  {
    "title": "ui.echart: 3D Graphing",
    "content": "Charts will automatically be 3D enabled if the initial options contain the string \"3D\".\nIf not, set the `enable_3d` argument to `True`.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.echart({\n    'xAxis3D': {},\n    'yAxis3D': {},\n    'zAxis3D': {},\n    'grid3D': {},\n    'series': [{\n        'type': 'line3D',\n        'data': [[1, 1, 1], [3, 3, 3]],\n    }],\n})\n\nui.run()",
    "url": "/documentation/echart#3d_graphing"
  },
  {
    "title": "ui.echart: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/echart#reference"
  },
  {
    "title": "ui.editor: Editor",
    "content": "A WYSIWYG editor based on `Quasar's QEditor \u003Chttps://quasar.dev/vue-components/editor\u003E`_.\nThe value is a string containing the formatted text as HTML code.\n\n:param value: initial value\n:param on_change: callback to be invoked when the value changes\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\neditor = ui.editor(placeholder='Type something here')\nui.markdown().bind_content_from(editor, 'value',\n                                backward=lambda v: f'HTML code:\\n```\\n{v}\\n```')\n\nui.run()",
    "url": "/documentation/editor#editor"
  },
  {
    "title": "ui.editor: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/editor#reference"
  },
  {
    "title": "ui.highchart: Highcharts chart",
    "content": "An element to create a chart using `Highcharts \u003Chttps://www.highcharts.com/\u003E`_.\nUpdates can be pushed to the chart by changing the `options` property.\nAfter data has changed, call the `update` method to refresh the chart.\n\nDue to Highcharts' restrictive license, this element is not part of the standard NiceGUI package.\nIt is maintained in a `separate repository \u003Chttps://github.com/zauberzeug/nicegui-highcharts/\u003E`_\nand can be installed with `pip install nicegui[highcharts]`.\n\nBy default, a `Highcharts.chart` is created.\nTo use, e.g., `Highcharts.stockChart` instead, set the `type` property to \"stockChart\".\n\n:param options: dictionary of Highcharts options\n:param type: chart type (e.g. \"chart\", \"stockChart\", \"mapChart\", ...; default: \"chart\")\n:param extras: list of extra dependencies to include (e.g. \"annotations\", \"arc-diagram\", \"solid-gauge\", ...)\n:param on_point_click: callback function that is called when a point is clicked\n:param on_point_drag_start: callback function that is called when a point drag starts\n:param on_point_drag: callback function that is called when a point is dragged\n:param on_point_drop: callback function that is called when a point is dropped\n",
    "format": "rst",
    "demo": "from nicegui import ui\nfrom random import random\n\nchart = ui.highchart({\n    'title': False,\n    'chart': {'type': 'bar'},\n    'xAxis': {'categories': ['A', 'B']},\n    'series': [\n        {'name': 'Alpha', 'data': [0.1, 0.2]},\n        {'name': 'Beta', 'data': [0.3, 0.4]},\n    ],\n}).classes('w-full h-64')\n\ndef update():\n    chart.options['series'][0]['data'][0] = random()\n    chart.update()\n\nui.button('Update', on_click=update)\n\nui.run()",
    "url": "/documentation/highchart#highcharts_chart"
  },
  {
    "title": "ui.highchart: Chart with extra dependencies",
    "content": "To use a chart type that is not included in the default dependencies, you can specify extra dependencies.\nThis demo shows a solid gauge chart.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.highchart({\n    'title': False,\n    'chart': {'type': 'solidgauge'},\n    'yAxis': {\n        'min': 0,\n        'max': 1,\n    },\n    'series': [\n        {'data': [0.42]},\n    ],\n}, extras=['solid-gauge']).classes('w-full h-64')\n\nui.run()",
    "url": "/documentation/highchart#chart_with_extra_dependencies"
  },
  {
    "title": "ui.highchart: Chart with draggable points",
    "content": "This chart allows dragging the series points.\nYou can register callbacks for the following events:\n\n- `on_point_click`: called when a point is clicked\n- `on_point_drag_start`: called when a point drag starts\n- `on_point_drag`: called when a point is dragged\n- `on_point_drop`: called when a point is dropped",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.highchart(\n    {\n        'title': False,\n        'plotOptions': {\n            'series': {\n                'stickyTracking': False,\n                'dragDrop': {'draggableY': True, 'dragPrecisionY': 1},\n            },\n        },\n        'series': [\n            {'name': 'A', 'data': [[20, 10], [30, 20], [40, 30]]},\n            {'name': 'B', 'data': [[50, 40], [60, 50], [70, 60]]},\n        ],\n    },\n    extras=['draggable-points'],\n    on_point_click=lambda e: ui.notify(f'Click: {e}'),\n    on_point_drag_start=lambda e: ui.notify(f'Drag start: {e}'),\n    on_point_drop=lambda e: ui.notify(f'Drop: {e}')\n).classes('w-full h-64')\n\nui.run()",
    "url": "/documentation/highchart#chart_with_draggable_points"
  },
  {
    "title": "ui.highchart: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/highchart#reference"
  },
  {
    "title": "ui.json_editor: JSONEditor",
    "content": "An element to create a JSON editor using `JSONEditor \u003Chttps://github.com/josdejong/svelte-jsoneditor\u003E`_.\nUpdates can be pushed to the editor by changing the `properties` property.\nAfter data has changed, call the `update` method to refresh the editor.\n\n:param properties: dictionary of JSONEditor properties\n:param on_select: callback which is invoked when some of the content has been selected\n:param on_change: callback which is invoked when the content has changed\n:param schema: optional `JSON schema \u003Chttps://json-schema.org/\u003E`_ for validating the data being edited (*added in version 2.8.0*)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\njson = {\n    'array': [1, 2, 3],\n    'boolean': True,\n    'color': '#82b92c',\n    None: None,\n    'number': 123,\n    'object': {\n        'a': 'b',\n        'c': 'd',\n    },\n    'time': 1575599819000,\n    'string': 'Hello World',\n}\nui.json_editor({'content': {'json': json}},\n               on_select=lambda e: ui.notify(f'Select: {e}'),\n               on_change=lambda e: ui.notify(f'Change: {e}'))\n\nui.run()",
    "url": "/documentation/json_editor#jsoneditor"
  },
  {
    "title": "ui.json_editor: Validation",
    "content": "You can use the `schema` parameter to define a [JSON schema](https://json-schema.org/) for validating the data being edited.\nIn this demo, the editor will warn if the data does not match the schema:\n\n- `id` must be an integer\n- `name` must be a string\n- `price` must be a number greater than 0\n\n*Added in version 2.8.0*",
    "format": "md",
    "demo": "from nicegui import ui\n\nschema = {\n    'type': 'object',\n    'properties': {\n        'id': {\n            'type': 'integer',\n        },\n        'name': {\n            'type': 'string',\n        },\n        'price': {\n            'type': 'number',\n            'exclusiveMinimum': 0,\n        },\n    },\n    'required': ['id', 'name', 'price'],\n}\ndata = {\n    'id': 42,\n    'name': 'Banana',\n    'price': 15.0,\n}\nui.json_editor({'content': {'json': data}}, schema=schema)\n\nui.run()",
    "url": "/documentation/json_editor#validation"
  },
  {
    "title": "ui.json_editor: Run methods",
    "content": "You can run methods of the JSONEditor instance using the `run_editor_method` method.\nThis demo shows how to expand and collapse all nodes and how to get the current data.\n\nThe colon \":\" in front of the method name \"expand\" indicates that the value \"path =\u003E true\" is a JavaScript expression\nthat is evaluated on the client before it is passed to the method.\n\nNote that requesting data from the client is only supported for page functions, not for the shared auto-index page.",
    "format": "md",
    "demo": "from nicegui import ui\n\n@ui.page('/')\ndef page():\n    json = {\n        'Name': 'Alice',\n        'Age': 42,\n        'Address': {\n            'Street': 'Main Street',\n            'City': 'Wonderland',\n        },\n    }\n    editor = ui.json_editor({'content': {'json': json}})\n\n    ui.button('Expand', on_click=lambda: editor.run_editor_method(':expand', 'path =\u003E true'))\n    ui.button('Collapse', on_click=lambda: editor.run_editor_method(':expand', 'path =\u003E false'))\n    ui.button('Readonly', on_click=lambda: editor.run_editor_method('updateProps', {'readOnly': True}))\n\n    async def get_data() -\u003E None:\n        data = await editor.run_editor_method('get')\n        ui.notify(data)\n    ui.button('Get Data', on_click=get_data)\n\nui.run()",
    "url": "/documentation/json_editor#run_methods"
  },
  {
    "title": "ui.json_editor: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/json_editor#reference"
  },
  {
    "title": "ui.leaflet: Leaflet map",
    "content": "This element is a wrapper around the `Leaflet \u003Chttps://leafletjs.com/\u003E`_ JavaScript library.\n\n:param center: initial center location of the map (latitude/longitude, default: (0.0, 0.0))\n:param zoom: initial zoom level of the map (default: 13)\n:param draw_control: whether to show the draw toolbar (default: False)\n:param options: additional options passed to the Leaflet map (default: {})\n:param hide_drawn_items: whether to hide drawn items on the map (default: False, *added in version 2.0.0*)\n:param additional_resources: additional resources like CSS or JS files to load (default: None, *added in version 2.11.0*)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nm = ui.leaflet(center=(51.505, -0.09))\nui.label().bind_text_from(m, 'center', lambda center: f'Center: {center[0]:.3f}, {center[1]:.3f}')\nui.label().bind_text_from(m, 'zoom', lambda zoom: f'Zoom: {zoom}')\n\nwith ui.grid(columns=2):\n    ui.button('London', on_click=lambda: m.set_center((51.505, -0.090)))\n    ui.button('Berlin', on_click=lambda: m.set_center((52.520, 13.405)))\n    ui.button(icon='zoom_in', on_click=lambda: m.set_zoom(m.zoom + 1))\n    ui.button(icon='zoom_out', on_click=lambda: m.set_zoom(m.zoom - 1))\n\nui.run()",
    "url": "/documentation/leaflet#leaflet_map"
  },
  {
    "title": "ui.leaflet: Changing the Map Style",
    "content": "The default map style is OpenStreetMap.\nYou can find more map styles at \u003Chttps://leaflet-extras.github.io/leaflet-providers/preview/\u003E.\nEach call to `tile_layer` stacks upon the previous ones.\nSo if you want to change the map style, you have to remove the default one first.\n\n*Updated in version 2.12.0: Both WMTS and WMS map services are supported.*",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.label('Web Map Tile Service')\nmap1 = ui.leaflet(center=(51.505, -0.090), zoom=3)\nmap1.clear_layers()\nmap1.tile_layer(\n    url_template=r'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',\n    options={\n        'maxZoom': 17,\n        'attribution':\n            'Map data: &copy; \u003Ca href=\"https://www.openstreetmap.org/copyright\"\u003EOpenStreetMap\u003C/a\u003E contributors, \u003Ca href=\"https://viewfinderpanoramas.org/\"\u003ESRTM\u003C/a\u003E | '\n            'Map style: &copy; \u003Ca href=\"https://opentopomap.org\"\u003EOpenTopoMap\u003C/a\u003E (\u003Ca href=\"https://creativecommons.org/licenses/by-sa/3.0/\"\u003ECC-BY-SA\u003C/a\u003E)'\n    },\n)\n\nui.label('Web Map Service')\nmap2 = ui.leaflet(center=(51.505, -0.090), zoom=3)\nmap2.clear_layers()\nmap2.wms_layer(\n    url_template='http://ows.mundialis.de/services/service?',\n    options={\n        'layers': 'TOPO-WMS,OSM-Overlay-WMS'\n    },\n)\n\nui.run()",
    "url": "/documentation/leaflet#changing_the_map_style"
  },
  {
    "title": "ui.leaflet: Add Markers on Click",
    "content": "You can add markers to the map with `marker`.\nThe `center` argument is a tuple of latitude and longitude.\nThis demo adds markers by clicking on the map.\nNote that the \"map-click\" event refers to the click event of the map object,\nwhile the \"click\" event refers to the click event of the container div.",
    "format": "md",
    "demo": "from nicegui import events, ui\n\nm = ui.leaflet(center=(51.505, -0.09))\n\ndef handle_click(e: events.GenericEventArguments):\n    lat = e.args['latlng']['lat']\n    lng = e.args['latlng']['lng']\n    m.marker(latlng=(lat, lng))\nm.on('map-click', handle_click)\n\nui.run()",
    "url": "/documentation/leaflet#add_markers_on_click"
  },
  {
    "title": "ui.leaflet: Move Markers",
    "content": "You can move markers with the `move` method.",
    "format": "md",
    "demo": "from nicegui import ui\n\nm = ui.leaflet(center=(51.505, -0.09))\nmarker = m.marker(latlng=m.center)\nui.button('Move marker', on_click=lambda: marker.move(51.51, -0.09))\n\nui.run()",
    "url": "/documentation/leaflet#move_markers"
  },
  {
    "title": "ui.leaflet: Image Overlays",
    "content": "Leaflet supports [image overlays](https://leafletjs.com/reference.html#imageoverlay).\nYou can add an image overlay with the `image_overlay` method.\n\n*Added in version 2.17.0*",
    "format": "md",
    "demo": "from nicegui import ui\n\nm = ui.leaflet(center=(40.74, -74.18), zoom=11)\nm.image_overlay(\n    url='https://maps.lib.utexas.edu/maps/historical/newark_nj_1922.jpg',\n    bounds=[[40.712216, -74.22655], [40.773941, -74.12544]],\n    options={'opacity': 0.8},\n)\n\nui.run()",
    "url": "/documentation/leaflet#image_overlays"
  },
  {
    "title": "ui.leaflet: Video Overlays",
    "content": "Leaflet supports [video overlays](https://leafletjs.com/reference.html#videooverlay).\nYou can add a video overlay with the `video_overlay` method.\n\n*Added in version 2.17.0*",
    "format": "md",
    "demo": "from nicegui import ui\n\nm = ui.leaflet(center=(23.0, -115.0), zoom=3)\nm.video_overlay(\n    url='https://www.mapbox.com/bites/00188/patricia_nasa.webm',\n    bounds=[[32, -130], [13, -100]],\n    options={'opacity': 0.8, 'autoplay': True, 'playsInline': True},\n)\n\nui.run()",
    "url": "/documentation/leaflet#video_overlays"
  },
  {
    "title": "ui.leaflet: Vector Layers",
    "content": "Leaflet supports a set of [vector layers](https://leafletjs.com/reference.html#:~:text=VideoOverlay-,Vector%20Layers,-Path) like circle, polygon etc.\nThese can be added with the `generic_layer` method.\nWe are happy to review any pull requests to add more specific layers to simplify usage.",
    "format": "md",
    "demo": "from nicegui import ui\n\nm = ui.leaflet(center=(51.505, -0.09)).classes('h-32')\nm.generic_layer(name='circle', args=[m.center, {'color': 'red', 'radius': 300}])\n\nui.run()",
    "url": "/documentation/leaflet#vector_layers"
  },
  {
    "title": "ui.leaflet: Disable Pan and Zoom",
    "content": "There are [several options to configure the map in Leaflet](https://leafletjs.com/reference.html#map).\nThis demo disables the pan and zoom controls.",
    "format": "md",
    "demo": "from nicegui import ui\n\noptions = {\n    'zoomControl': False,\n    'scrollWheelZoom': False,\n    'doubleClickZoom': False,\n    'boxZoom': False,\n    'keyboard': False,\n    'dragging': False,\n}\nui.leaflet(center=(51.505, -0.09), options=options)\n\nui.run()",
    "url": "/documentation/leaflet#disable_pan_and_zoom"
  },
  {
    "title": "ui.leaflet: Draw on Map",
    "content": "You can enable a toolbar to draw on the map.\nThe `draw_control` can be used to configure the toolbar.\nThis demo adds markers and polygons by clicking on the map.\nBy setting \"edit\" and \"remove\" to `True` (the default), you can enable editing and deleting drawn shapes.",
    "format": "md",
    "demo": "from nicegui import events, ui\n\ndef handle_draw(e: events.GenericEventArguments):\n    layer_type = e.args['layerType']\n    coords = e.args['layer'].get('_latlng') or e.args['layer'].get('_latlngs')\n    ui.notify(f'Drawn a {layer_type} at {coords}')\n\ndraw_control = {\n    'draw': {\n        'polygon': True,\n        'marker': True,\n        'circle': True,\n        'rectangle': True,\n        'polyline': True,\n        'circlemarker': True,\n    },\n    'edit': {\n        'edit': True,\n        'remove': True,\n    },\n}\nm = ui.leaflet(center=(51.505, -0.09), draw_control=draw_control)\nm.classes('h-96')\nm.on('draw:created', handle_draw)\nm.on('draw:edited', lambda: ui.notify('Edit completed'))\nm.on('draw:deleted', lambda: ui.notify('Delete completed'))\n\nui.run()",
    "url": "/documentation/leaflet#draw_on_map"
  },
  {
    "title": "ui.leaflet: Draw with Custom Options",
    "content": "You can draw shapes with custom options like stroke color and weight.\nTo hide the default rendering of drawn items, set `hide_drawn_items` to `True`.",
    "format": "md",
    "demo": "from nicegui import events, ui\n\ndef handle_draw(e: events.GenericEventArguments):\n    options = {'color': 'red', 'weight': 1}\n    m.generic_layer(name='polygon', args=[e.args['layer']['_latlngs'], options])\n\ndraw_control = {\n    'draw': {\n        'polygon': True,\n        'marker': False,\n        'circle': False,\n        'rectangle': False,\n        'polyline': False,\n        'circlemarker': False,\n    },\n    'edit': {\n        'edit': False,\n        'remove': False,\n    },\n}\nm = ui.leaflet(center=(51.5, 0), draw_control=draw_control, hide_drawn_items=True)\nm.on('draw:created', handle_draw)\n\nui.run()",
    "url": "/documentation/leaflet#draw_with_custom_options"
  },
  {
    "title": "ui.leaflet: Run Map Methods",
    "content": "You can run methods of the Leaflet map object with `run_map_method`.\nThis demo shows how to fit the map to the whole world.",
    "format": "md",
    "demo": "from nicegui import ui\n\nm = ui.leaflet(center=(51.505, -0.09)).classes('h-32')\nui.button('Fit world', on_click=lambda: m.run_map_method('fitWorld'))\n\nui.run()",
    "url": "/documentation/leaflet#run_map_methods"
  },
  {
    "title": "ui.leaflet: Run Layer Methods",
    "content": "You can run methods of the Leaflet layer objects with `run_layer_method`.\nThis demo shows how to change the opacity of a marker or change its icon.",
    "format": "md",
    "demo": "from nicegui import ui\n\nm = ui.leaflet(center=(51.505, -0.09)).classes('h-32')\nmarker = m.marker(latlng=m.center)\nui.button('Hide', on_click=lambda: marker.run_method('setOpacity', 0.3))\nui.button('Show', on_click=lambda: marker.run_method('setOpacity', 1.0))\n\nicon = 'L.icon({iconUrl: \"https://leafletjs.com/examples/custom-icons/leaf-green.png\"})'\nui.button('Change icon', on_click=lambda: marker.run_method(':setIcon', icon))\n\nui.run()",
    "url": "/documentation/leaflet#run_layer_methods"
  },
  {
    "title": "ui.leaflet: Wait for Initialization",
    "content": "You can wait for the map to be initialized with the `initialized` method.\nThis is necessary when you want to run methods like fitting the bounds of the map right after the map is created.",
    "format": "md",
    "demo": "from nicegui import ui\n\n@ui.page('/')\nasync def page():\n    m = ui.leaflet(zoom=5)\n    central_park = m.generic_layer(name='polygon', args=[[\n        (40.767809, -73.981249),\n        (40.800273, -73.958291),\n        (40.797011, -73.949683),\n        (40.764704, -73.973741),\n    ]])\n    await m.initialized()\n    bounds = await central_park.run_method('getBounds')\n    m.run_map_method('fitBounds', [[bounds['_southWest'], bounds['_northEast']]])\n\nui.run()",
    "url": "/documentation/leaflet#wait_for_initialization"
  },
  {
    "title": "ui.leaflet: Leaflet Plugins",
    "content": "You can add plugins to the map by passing the URLs of JS and CSS files to the `additional_resources` parameter.\nThis demo shows how to add the [Leaflet.RotatedMarker](https://github.com/bbecquet/Leaflet.RotatedMarker) plugin.\nIt allows you to rotate markers by a given `rotationAngle`.\n\n*Added in version 2.11.0*",
    "format": "md",
    "demo": "from nicegui import ui\n\nm = ui.leaflet((51.51, -0.09), additional_resources=[\n    'https://unpkg.com/leaflet-rotatedmarker@0.2.0/leaflet.rotatedMarker.js',\n])\nm.marker(latlng=(51.51, -0.091), options={'rotationAngle': -30})\nm.marker(latlng=(51.51, -0.090), options={'rotationAngle': 30})\n\nui.run()",
    "url": "/documentation/leaflet#leaflet_plugins"
  },
  {
    "title": "ui.leaflet: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/leaflet#reference"
  },
  {
    "title": "ui.line_plot: Line Plot",
    "content": "Create a line plot using pyplot.\nThe `push` method provides live updating when utilized in combination with `ui.timer`.\n\n:param n: number of lines\n:param limit: maximum number of datapoints per line (new points will displace the oldest)\n:param update_every: update plot only after pushing new data multiple times to save CPU and bandwidth\n:param close: whether the figure should be closed after exiting the context; set to `False` if you want to update it later (default: `True`)\n:param kwargs: arguments like `figsize` which should be passed to `pyplot.figure \u003Chttps://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.figure.html\u003E`_\n",
    "format": "rst",
    "demo": "import math\nfrom datetime import datetime\nfrom nicegui import ui\n\nline_plot = ui.line_plot(n=2, limit=20, figsize=(3, 2), update_every=5) \\\n    .with_legend(['sin', 'cos'], loc='upper center', ncol=2)\n\ndef update_line_plot() -\u003E None:\n    now = datetime.now()\n    x = now.timestamp()\n    y1 = math.sin(x)\n    y2 = math.cos(x)\n    line_plot.push([now], [[y1], [y2]], y_limits=(-1.5, 1.5))\n\nline_updates = ui.timer(0.1, update_line_plot, active=False)\nline_checkbox = ui.checkbox('active').bind_value(line_updates, 'active')\n\nui.run()",
    "url": "/documentation/line_plot#line_plot"
  },
  {
    "title": "ui.line_plot: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/line_plot#reference"
  },
  {
    "title": "ui.linear_progress: Linear Progress",
    "content": "A linear progress bar wrapping Quasar's\n`QLinearProgress \u003Chttps://quasar.dev/vue-components/linear-progress\u003E`_ component.\n\n:param value: the initial value of the field (from 0.0 to 1.0)\n:param size: the height of the progress bar (default: \"20px\" with value label and \"4px\" without)\n:param show_value: whether to show a value label in the center (default: `True`)\n:param color: color (either a Quasar, Tailwind, or CSS color or `None`, default: \"primary\")\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nslider = ui.slider(min=0, max=1, step=0.01, value=0.5)\nui.linear_progress().bind_value_from(slider, 'value')\n\nui.run()",
    "url": "/documentation/linear_progress#linear_progress"
  },
  {
    "title": "ui.linear_progress: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/linear_progress#reference"
  },
  {
    "title": "ui.log: Log View",
    "content": "Create a log view that allows to add new lines without re-transmitting the whole history to the client.\n\n:param max_lines: maximum number of lines before dropping oldest ones (default: `None`)\n",
    "format": "rst",
    "demo": "from datetime import datetime\nfrom nicegui import ui\n\nlog = ui.log(max_lines=10).classes('w-full h-20')\nui.button('Log time', on_click=lambda: log.push(datetime.now().strftime('%X.%f')[:-5]))\n\nui.run()",
    "url": "/documentation/log#log_view"
  },
  {
    "title": "ui.log: Attach to a logger",
    "content": "You can attach a `ui.log` element to a Python logger object so that log messages are pushed to the log element.\nWhen used inside a page function, it is important to remove the handler when the client disconnects.\nOtherwise, the handler will keep a reference to the log element and the latter will not be garbage collected.",
    "format": "md",
    "demo": "import logging\nfrom datetime import datetime\nfrom nicegui import ui\n\nlogger = logging.getLogger()\n\nclass LogElementHandler(logging.Handler):\n    \"\"\"A logging handler that emits messages to a log element.\"\"\"\n\n    def __init__(self, element: ui.log, level: int = logging.NOTSET) -\u003E None:\n        self.element = element\n        super().__init__(level)\n\n    def emit(self, record: logging.LogRecord) -\u003E None:\n        try:\n            msg = self.format(record)\n            self.element.push(msg)\n        except Exception:\n            self.handleError(record)\n\n@ui.page('/')\ndef page():\n    log = ui.log(max_lines=10).classes('w-full')\n    handler = LogElementHandler(log)\n    logger.addHandler(handler)\n    ui.context.client.on_disconnect(lambda: logger.removeHandler(handler))\n    ui.button('Log time', on_click=lambda: logger.warning(datetime.now().strftime('%X.%f')[:-5]))\n\nui.run()",
    "url": "/documentation/log#attach_to_a_logger"
  },
  {
    "title": "ui.log: Styling lines",
    "content": "On the basis that individual lines in `ui.log` are `ui.label` instances,\nit is possible to style the inserted lines via `classes`, `style` and `props`.\nOne notable use would be colored logs.\n\nNote that if applied, this would clear any existing\n[classes](element#default_classes),\n[style](element#default_style), and\n[props](element#default_props)\ncurrently set as default on `ui.label`.\n\n*Added in version 2.18.0*",
    "format": "md",
    "demo": "from nicegui import ui\n\nlog = ui.log(max_lines=10).classes('w-full h-40')\nwith ui.row():\n    ui.button('Normal', on_click=lambda: log.push('Text'))\n    ui.button('Debug', on_click=lambda: log.push('Debug', classes='text-grey'))\n    ui.button('Info', on_click=lambda: log.push('Info', classes='text-blue'))\n    ui.button('Warning', on_click=lambda: log.push('Warning', classes='text-orange'))\n    ui.button('Error', on_click=lambda: log.push('Error', classes='text-red'))\n\nui.run()",
    "url": "/documentation/log#styling_lines"
  },
  {
    "title": "ui.log: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/log#reference"
  },
  {
    "title": "ui.matplotlib: Matplotlib",
    "content": "Create a `Matplotlib \u003Chttps://matplotlib.org/\u003E`_ element rendering a Matplotlib figure.\nThe figure is automatically updated when leaving the figure context.\n\n:param kwargs: arguments like `figsize` which should be passed to `matplotlib.figure.Figure \u003Chttps://matplotlib.org/stable/api/figure_api.html#matplotlib.figure.Figure\u003E`_\n",
    "format": "rst",
    "demo": "import numpy as np\nfrom nicegui import ui\n\nwith ui.matplotlib(figsize=(3, 2)).figure as fig:\n    x = np.linspace(0.0, 5.0)\n    y = np.cos(2 * np.pi * x) * np.exp(-x)\n    ax = fig.gca()\n    ax.plot(x, y, '-')\n\nui.run()",
    "url": "/documentation/matplotlib#matplotlib"
  },
  {
    "title": "ui.matplotlib: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/matplotlib#reference"
  },
  {
    "title": "ui.plotly: Plotly Element",
    "content": "Renders a Plotly chart.\nThere are two ways to pass a Plotly figure for rendering, see parameter `figure`:\n\n* Pass a `go.Figure` object, see https://plotly.com/python/\n\n* Pass a Python `dict` object with keys `data`, `layout`, `config` (optional), see https://plotly.com/javascript/\n\nFor best performance, use the declarative `dict` approach for creating a Plotly chart.\n\n:param figure: Plotly figure to be rendered. Can be either a `go.Figure` instance, or\n               a `dict` object with keys `data`, `layout`, `config` (optional).\n",
    "format": "rst",
    "demo": "import plotly.graph_objects as go\nfrom nicegui import ui\n\nfig = go.Figure(go.Scatter(x=[1, 2, 3, 4], y=[1, 2, 3, 2.5]))\nfig.update_layout(margin=dict(l=0, r=0, t=0, b=0))\nui.plotly(fig).classes('w-full h-40')\n\nui.run()",
    "url": "/documentation/plotly#plotly_element"
  },
  {
    "title": "ui.plotly: Dictionary interface",
    "content": "This demo shows how to use the declarative dictionary interface to create a plot.\nFor plots with many traces and data points, this is more efficient than the object-oriented interface.\nThe definition corresponds to the [JavaScript Plotly API](https://plotly.com/javascript/).\nDue to different defaults, the resulting plot may look slightly different from the same plot created with the object-oriented interface,\nbut the functionality is the same.",
    "format": "md",
    "demo": "from nicegui import ui\n\nfig = {\n    'data': [\n        {\n            'type': 'scatter',\n            'name': 'Trace 1',\n            'x': [1, 2, 3, 4],\n            'y': [1, 2, 3, 2.5],\n        },\n        {\n            'type': 'scatter',\n            'name': 'Trace 2',\n            'x': [1, 2, 3, 4],\n            'y': [1.4, 1.8, 3.8, 3.2],\n            'line': {'dash': 'dot', 'width': 3},\n        },\n    ],\n    'layout': {\n        'margin': {'l': 15, 'r': 0, 't': 0, 'b': 15},\n        'plot_bgcolor': '#E5ECF6',\n        'xaxis': {'gridcolor': 'white'},\n        'yaxis': {'gridcolor': 'white'},\n    },\n}\nui.plotly(fig).classes('w-full h-40')\n\nui.run()",
    "url": "/documentation/plotly#dictionary_interface"
  },
  {
    "title": "ui.plotly: Plot updates",
    "content": "This demo shows how to update the plot in real time.\nClick the button to add a new trace to the plot.\nTo send the new plot to the browser, make sure to explicitly call `plot.update()` or `ui.update(plot)`.",
    "format": "md",
    "demo": "import plotly.graph_objects as go\nfrom nicegui import ui\nfrom random import random\n\nfig = go.Figure()\nfig.update_layout(margin=dict(l=0, r=0, t=0, b=0))\nplot = ui.plotly(fig).classes('w-full h-40')\n\ndef add_trace():\n    fig.add_trace(go.Scatter(x=[1, 2, 3], y=[random(), random(), random()]))\n    plot.update()\n\nui.button('Add trace', on_click=add_trace)\n\nui.run()",
    "url": "/documentation/plotly#plot_updates"
  },
  {
    "title": "ui.plotly: Plot events",
    "content": "This demo shows how to handle Plotly events.\nTry clicking on a data point to see the event data.\n\nCurrently, the following events are supported:\n\"plotly\\_click\",\n\"plotly\\_legendclick\",\n\"plotly\\_selecting\",\n\"plotly\\_selected\",\n\"plotly\\_hover\",\n\"plotly\\_unhover\",\n\"plotly\\_legenddoubleclick\",\n\"plotly\\_restyle\",\n\"plotly\\_relayout\",\n\"plotly\\_webglcontextlost\",\n\"plotly\\_afterplot\",\n\"plotly\\_autosize\",\n\"plotly\\_deselect\",\n\"plotly\\_doubleclick\",\n\"plotly\\_redraw\",\n\"plotly\\_animated\".\nFor more information, see the [Plotly documentation](https://plotly.com/javascript/plotlyjs-events/).",
    "format": "md",
    "demo": "import plotly.graph_objects as go\nfrom nicegui import ui\n\nfig = go.Figure(go.Scatter(x=[1, 2, 3, 4], y=[1, 2, 3, 2.5]))\nfig.update_layout(margin=dict(l=0, r=0, t=0, b=0))\nplot = ui.plotly(fig).classes('w-full h-40')\nplot.on('plotly_click', ui.notify)\n\nui.run()",
    "url": "/documentation/plotly#plot_events"
  },
  {
    "title": "ui.plotly: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/plotly#reference"
  },
  {
    "title": "ui.pyplot: Pyplot Context",
    "content": "Create a context to configure a `Matplotlib \u003Chttps://matplotlib.org/\u003E`_ plot.\n\n:param close: whether the figure should be closed after exiting the context; set to `False` if you want to update it later (default: `True`)\n:param kwargs: arguments like `figsize` which should be passed to `pyplot.figure \u003Chttps://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.figure.html\u003E`_\n",
    "format": "rst",
    "demo": "import numpy as np\nfrom matplotlib import pyplot as plt\nfrom nicegui import ui\n\nwith ui.pyplot(figsize=(3, 2)):\n    x = np.linspace(0.0, 5.0)\n    y = np.cos(2 * np.pi * x) * np.exp(-x)\n    plt.plot(x, y, '-')\n\nui.run()",
    "url": "/documentation/pyplot#pyplot_context"
  },
  {
    "title": "ui.pyplot: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/pyplot#reference"
  },
  {
    "title": "ui.scene: 3D Scene",
    "content": "Display a 3D scene using `three.js \u003Chttps://threejs.org/\u003E`_.\nCurrently NiceGUI supports boxes, spheres, cylinders/cones, extrusions, straight lines, curves and textured meshes.\nObjects can be translated, rotated and displayed with different color, opacity or as wireframes.\nThey can also be grouped to apply joint movements.\n\n:param width: width of the canvas\n:param height: height of the canvas\n:param grid: whether to display a grid (boolean or tuple of ``size`` and ``divisions`` for `Three.js' GridHelper \u003Chttps://threejs.org/docs/#api/en/helpers/GridHelper\u003E`_, default: 100x100)\n:param camera: camera definition, either instance of ``ui.scene.perspective_camera`` (default) or ``ui.scene.orthographic_camera``\n:param on_click: callback to execute when a 3D object is clicked (use ``click_events`` to specify which events to subscribe to)\n:param click_events: list of JavaScript click events to subscribe to (default: ``['click', 'dblclick']``)\n:param on_drag_start: callback to execute when a 3D object is dragged\n:param on_drag_end: callback to execute when a 3D object is dropped\n:param drag_constraints: comma-separated JavaScript expression for constraining positions of dragged objects (e.g. ``'x = 0, z = y / 2'``)\n:param background_color: background color of the scene (default: \"#eee\")\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.scene().classes('w-full h-64') as scene:\n    scene.axes_helper()\n    scene.sphere().material('#4488ff').move(2, 2)\n    scene.cylinder(1, 0.5, 2, 20).material('#ff8800', opacity=0.5).move(-2, 1)\n    scene.extrusion([[0, 0], [0, 1], [1, 0.5]], 0.1).material('#ff8888').move(2, -1)\n\n    with scene.group().move(z=2):\n        scene.box().move(x=2)\n        scene.box().move(y=2).rotate(0.25, 0.5, 0.75)\n        scene.box(wireframe=True).material('#888888').move(x=2, y=2)\n\n    scene.line([-4, 0, 0], [-4, 2, 0]).material('#ff0000')\n    scene.curve([-4, 0, 0], [-4, -1, 0], [-3, -1, 0], [-3, 0, 0]).material('#008800')\n\n    logo = 'https://avatars.githubusercontent.com/u/2843826'\n    scene.texture(logo, [[[0.5, 2, 0], [2.5, 2, 0]],\n                         [[0.5, 0, 0], [2.5, 0, 0]]]).move(1, -3)\n\n    teapot = 'https://upload.wikimedia.org/wikipedia/commons/9/93/Utah_teapot_(solid).stl'\n    scene.stl(teapot).scale(0.2).move(-3, 4)\n\n    avocado = 'https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Assets/main/Models/Avocado/glTF-Binary/Avocado.glb'\n    scene.gltf(avocado).scale(40).move(-2, -3, 0.5)\n\n    scene.text('2D', 'background: rgba(0, 0, 0, 0.2); border-radius: 5px; padding: 5px').move(z=2)\n    scene.text3d('3D', 'background: rgba(0, 0, 0, 0.2); border-radius: 5px; padding: 5px').move(y=-2).scale(.05)\n\nui.run()",
    "url": "/documentation/scene#3d_scene"
  },
  {
    "title": "ui.scene: Handling Click Events",
    "content": "You can use the `on_click` argument to `ui.scene` to handle click events.\nThe callback receives a `SceneClickEventArguments` object with the following attributes:\n\n- `click_type`: the type of click (\"click\" or \"dblclick\").\n- `button`: the button that was clicked (1, 2, or 3).\n- `alt`, `ctrl`, `meta`, `shift`: whether the alt, ctrl, meta, or shift key was pressed.\n- `hits`: a list of `SceneClickEventHit` objects, sorted by distance from the camera.\n\nThe `SceneClickEventHit` object has the following attributes:\n\n- `object_id`: the id of the object that was clicked.\n- `object_name`: the name of the object that was clicked.\n- `x`, `y`, `z`: the x, y and z coordinates of the click.",
    "format": "md",
    "demo": "from nicegui import events, ui\n\ndef handle_click(e: events.SceneClickEventArguments):\n    hit = e.hits[0]\n    name = hit.object_name or hit.object_id\n    ui.notify(f'You clicked on the {name} at ({hit.x:.2f}, {hit.y:.2f}, {hit.z:.2f})')\n\nwith ui.scene(width=285, height=220, on_click=handle_click) as scene:\n    scene.sphere().move(x=-1, z=1).with_name('sphere')\n    scene.box().move(x=1, z=1).with_name('box')\n\nui.run()",
    "url": "/documentation/scene#handling_click_events"
  },
  {
    "title": "ui.scene: Context menu for 3D objects",
    "content": "This demo shows how to create a context menu for 3D objects.\nBy setting the `click_events` argument to `['contextmenu']`, the `handle_click` function will be called on right-click.\nIt clears the context menu and adds items based on the object that was clicked.",
    "format": "md",
    "demo": "from nicegui import events, ui\n\ndef handle_click(e: events.SceneClickEventArguments) -\u003E None:\n    context_menu.clear()\n    name = next((hit.object_name for hit in e.hits if hit.object_name), None)\n    with context_menu:\n        if name == 'sphere':\n            ui.item('SPHERE').classes('font-bold')\n            ui.menu_item('inspect')\n            ui.menu_item('open')\n        if name == 'box':\n            ui.item('BOX').classes('font-bold')\n            ui.menu_item('rotate')\n            ui.menu_item('move')\n\nwith ui.element():\n    context_menu = ui.context_menu()\n    with ui.scene(width=285, height=220, on_click=handle_click,\n                  click_events=['contextmenu']) as scene:\n        scene.sphere().move(x=-1, z=1).with_name('sphere')\n        scene.box().move(x=1, z=1).with_name('box')\n\nui.run()",
    "url": "/documentation/scene#context_menu_for_3d_objects"
  },
  {
    "title": "ui.scene: Draggable objects",
    "content": "You can make objects draggable using the `.draggable` method.\nThere is an optional `on_drag_start` and `on_drag_end` argument to `ui.scene` to handle drag events.\nThe callbacks receive a `SceneDragEventArguments` object with the following attributes:\n\n- `type`: the type of drag event (\"dragstart\" or \"dragend\").\n- `object_id`: the id of the object that was dragged.\n- `object_name`: the name of the object that was dragged.\n- `x`, `y`, `z`: the x, y and z coordinates of the dragged object.\n\nYou can also use the `drag_constraints` argument to set comma-separated JavaScript expressions\nfor constraining positions of dragged objects.",
    "format": "md",
    "demo": "from nicegui import events, ui\n\ndef handle_drag(e: events.SceneDragEventArguments):\n    ui.notify(f'You dropped the sphere at ({e.x:.2f}, {e.y:.2f}, {e.z:.2f})')\n\nwith ui.scene(width=285, height=220,\n              drag_constraints='z = 1', on_drag_end=handle_drag) as scene:\n    sphere = scene.sphere().move(z=1).draggable()\n\nui.switch('draggable sphere',\n          value=sphere.draggable_,\n          on_change=lambda e: sphere.draggable(e.value))\n\nui.run()",
    "url": "/documentation/scene#draggable_objects"
  },
  {
    "title": "ui.scene: Subscribe to the drag event",
    "content": "By default, a draggable object is only updated when the drag ends to avoid performance issues.\nBut you can explicitly subscribe to the \"drag\" event to get immediate updates.\nIn this demo we update the position and size of a box based on the positions of two draggable spheres.",
    "format": "md",
    "demo": "from nicegui import events, ui\n\nwith ui.scene(width=285, drag_constraints='z=0') as scene:\n    box = scene.box(1, 1, 0.2).move(0, 0).material('Orange')\n    sphere1 = scene.sphere(0.2).move(0.5, -0.5).material('SteelBlue').draggable()\n    sphere2 = scene.sphere(0.2).move(-0.5, 0.5).material('SteelBlue').draggable()\n\ndef handle_drag(e: events.GenericEventArguments) -\u003E None:\n    x1 = sphere1.x if e.args['object_id'] == sphere2.id else e.args['x']\n    y1 = sphere1.y if e.args['object_id'] == sphere2.id else e.args['y']\n    x2 = sphere2.x if e.args['object_id'] == sphere1.id else e.args['x']\n    y2 = sphere2.y if e.args['object_id'] == sphere1.id else e.args['y']\n    box.move((x1 + x2) / 2, (y1 + y2) / 2).scale(x2 - x1, y2 - y1, 1)\nscene.on('drag', handle_drag)\n\nui.run()",
    "url": "/documentation/scene#subscribe_to_the_drag_event"
  },
  {
    "title": "ui.scene: Rendering point clouds",
    "content": "You can render point clouds using the `point_cloud` method.\nThe `points` argument is a list of point coordinates, and the `colors` argument is a list of RGB colors (0..1).\nYou can update the cloud using its `set_points()` method.",
    "format": "md",
    "demo": "import numpy as np\nfrom nicegui import ui\n\ndef generate_data(frequency: float = 1.0):\n    x, y = np.meshgrid(np.linspace(-3, 3), np.linspace(-3, 3))\n    z = np.sin(x * frequency) * np.cos(y * frequency) + 1\n    points = np.dstack([x, y, z]).reshape(-1, 3)\n    colors = points / [6, 6, 2] + [0.5, 0.5, 0]\n    return points, colors\n\nwith ui.scene().classes('w-full h-64') as scene:\n    points, colors = generate_data()\n    point_cloud = scene.point_cloud(points, colors, point_size=0.1)\n\nui.slider(min=0.1, max=3, step=0.1, value=1) \\\n    .on_value_change(lambda e: point_cloud.set_points(*generate_data(e.value)))\n\nui.run()",
    "url": "/documentation/scene#rendering_point_clouds"
  },
  {
    "title": "ui.scene: Wait for Initialization",
    "content": "You can wait for the scene to be initialized with the `initialized` method.\nThis demo animates a camera movement after the scene has been fully loaded.",
    "format": "md",
    "demo": "from nicegui import ui\n\n@ui.page('/')\nasync def page():\n    with ui.scene(width=285, height=220) as scene:\n        scene.sphere()\n        await scene.initialized()\n        scene.move_camera(x=1, y=-1, z=1.5, duration=2)\n\nui.run()",
    "url": "/documentation/scene#wait_for_initialization"
  },
  {
    "title": "ui.scene: Scene View",
    "content": "Display an additional view of a 3D scene using `three.js \u003Chttps://threejs.org/\u003E`_.\nThis component can only show a scene and not modify it.\nYou can, however, independently move the camera.\n\nCurrent limitation: 2D and 3D text objects are not supported and will not be displayed in the scene view.\n\n:param scene: the scene which will be shown on the canvas\n:param width: width of the canvas\n:param height: height of the canvas\n:param camera: camera definition, either instance of ``ui.scene.perspective_camera`` (default) or ``ui.scene.orthographic_camera``\n:param on_click: callback to execute when a 3D object is clicked\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.grid(columns=2).classes('w-full'):\n    with ui.scene().classes('h-64 col-span-2') as scene:\n        teapot = 'https://upload.wikimedia.org/wikipedia/commons/9/93/Utah_teapot_(solid).stl'\n        scene.stl(teapot).scale(0.3)\n\n    with ui.scene_view(scene).classes('h-32') as scene_view1:\n        scene_view1.move_camera(x=1, y=-3, z=5)\n\n    with ui.scene_view(scene).classes('h-32') as scene_view2:\n        scene_view2.move_camera(x=0, y=4, z=3)\n\nui.run()",
    "url": "/documentation/scene#scene_view"
  },
  {
    "title": "ui.scene: Camera Parameters",
    "content": "You can use the `camera` argument to `ui.scene` to use a custom camera.\nThis allows you to set the field of view of a perspective camera or the size of an orthographic camera.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.scene(camera=ui.scene.orthographic_camera(size=2)) \\\n        .classes('w-full h-64') as scene:\n    scene.box()\n\nui.run()",
    "url": "/documentation/scene#camera_parameters"
  },
  {
    "title": "ui.scene: Get current camera pose",
    "content": "Using the `get_camera` method you can get a dictionary of current camera parameters like position, rotation, field of view and more.\nThis demo shows how to continuously move a sphere towards the camera.\nTry moving the camera around to see the sphere following it.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.scene().classes('w-full h-64') as scene:\n    ball = scene.sphere()\n\nasync def move():\n    camera = await scene.get_camera()\n    if camera is not None:\n        ball.move(x=0.95 * ball.x + 0.05 * camera['position']['x'],\n                  y=0.95 * ball.y + 0.05 * camera['position']['y'],\n                  z=1.0)\nui.timer(0.1, move)\n\nui.run()",
    "url": "/documentation/scene#get_current_camera_pose"
  },
  {
    "title": "ui.scene: Custom Background",
    "content": "You can set a custom background color using the `background_color` parameter of `ui.scene`.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.scene(background_color='#222').classes('w-full h-64') as scene:\n    scene.box()\n\nui.run()",
    "url": "/documentation/scene#custom_background"
  },
  {
    "title": "ui.scene: Custom Grid",
    "content": "You can set custom grid parameters using the `grid` parameter of `ui.scene`.\nIt accepts a tuple of two integers, the first one for the grid size and the second one for the number of divisions.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.scene(grid=(3, 2)).classes('w-full h-64') as scene:\n    scene.sphere()\n\nui.run()",
    "url": "/documentation/scene#custom_grid"
  },
  {
    "title": "ui.scene: Custom Composed 3D Objects",
    "content": "This demo creates a custom class for visualizing a coordinate system with colored X, Y and Z axes.\nThis can be a nice alternative to the default `axes_helper` object.",
    "format": "md",
    "demo": "import math\nfrom nicegui import ui\n\nclass CoordinateSystem(ui.scene.group):\n\n    def __init__(self, name: str, *, length: float = 1.0) -\u003E None:\n        super().__init__()\n\n        with self:\n            for label, color, rx, ry, rz in [\n                ('x', '#ff0000', 0, 0, -math.pi / 2),\n                ('y', '#00ff00', 0, 0, 0),\n                ('z', '#0000ff', math.pi / 2, 0, 0),\n            ]:\n                with ui.scene.group().rotate(rx, ry, rz):\n                    ui.scene.cylinder(0.02 * length, 0.02 * length, 0.8 * length) \\\n                        .move(y=0.4 * length).material(color)\n                    ui.scene.cylinder(0, 0.1 * length, 0.2 * length) \\\n                        .move(y=0.9 * length).material(color)\n                    ui.scene.text(label, style=f'color: {color}') \\\n                        .move(y=1.1 * length)\n            ui.scene.text(name, style='color: #808080')\n\nwith ui.scene().classes('w-full h-64'):\n    CoordinateSystem('origin')\n    CoordinateSystem('custom frame').move(-2, -2, 1).rotate(0.1, 0.2, 0.3)\n\nui.run()",
    "url": "/documentation/scene#custom_composed_3d_objects"
  },
  {
    "title": "ui.scene: Attaching/detaching objects",
    "content": "To add or remove objects from groups you can use the `attach` and `detach` methods.\nThe position and rotation of the object are preserved so that the object does not move in space.\nBut note that scaling is not preserved.\nIf either the parent or the object itself is scaled, the object shape and position can change.\n\n*Added in version 2.7.0*",
    "format": "md",
    "demo": "import math\nimport time\nfrom nicegui import ui\n\nwith ui.scene().classes('w-full h-64') as scene:\n    with scene.group() as group:\n        a = scene.box().move(-2)\n        b = scene.box().move(0)\n        c = scene.box().move(2)\n\nui.timer(0.1, lambda: group.move(y=math.sin(time.time())).rotate(0, 0, time.time()))\nui.button('Detach', on_click=a.detach)\nui.button('Attach', on_click=lambda: a.attach(group))\n\nui.run()",
    "url": "/documentation/scene#attaching_detaching_objects"
  },
  {
    "title": "ui.scene: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/scene#reference"
  },
  {
    "title": "ui.spinner: Spinner",
    "content": "This element is based on Quasar's `QSpinner \u003Chttps://quasar.dev/vue-components/spinners\u003E`_ component.\n\n:param type: type of spinner (e.g. \"audio\", \"ball\", \"bars\", ..., default: \"default\")\n:param size: size of the spinner (e.g. \"3em\", \"10px\", \"xl\", ..., default: \"1em\")\n:param color: color of the spinner (either a Quasar, Tailwind, or CSS color or `None`, default: \"primary\")\n:param thickness: thickness of the spinner (applies to the \"default\" spinner only, default: 5.0)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.row():\n    ui.spinner(size='lg')\n    ui.spinner('audio', size='lg', color='green')\n    ui.spinner('dots', size='lg', color='red')\n\nui.run()",
    "url": "/documentation/spinner#spinner"
  },
  {
    "title": "ui.spinner: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/spinner#reference"
  },
  {
    "title": "ui.table: Table",
    "content": "A table based on Quasar's `QTable \u003Chttps://quasar.dev/vue-components/table\u003E`_ component.\n\n:param rows: list of row objects\n:param columns: list of column objects (defaults to the columns of the first row *since version 2.0.0*)\n:param column_defaults: optional default column properties, *added in version 2.0.0*\n:param row_key: name of the column containing unique data identifying the row (default: \"id\")\n:param title: title of the table\n:param selection: selection type (\"single\" or \"multiple\"; default: `None`)\n:param pagination: a dictionary correlating to a pagination object or number of rows per page (`None` hides the pagination, 0 means \"infinite\"; default: `None`).\n:param on_select: callback which is invoked when the selection changes\n:param on_pagination_change: callback which is invoked when the pagination changes\n\nIf selection is 'single' or 'multiple', then a `selected` property is accessible containing the selected rows.\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\ncolumns = [\n    {'name': 'name', 'label': 'Name', 'field': 'name', 'required': True, 'align': 'left'},\n    {'name': 'age', 'label': 'Age', 'field': 'age', 'sortable': True},\n]\nrows = [\n    {'name': 'Alice', 'age': 18},\n    {'name': 'Bob', 'age': 21},\n    {'name': 'Carol'},\n]\nui.table(columns=columns, rows=rows, row_key='name')\n\nui.run()",
    "url": "/documentation/table#table"
  },
  {
    "title": "ui.table: Omitting columns",
    "content": "If you omit the `columns` parameter, the table will automatically generate columns from the first row.\nLabels are uppercased and sorting is enabled.\n\n*Updated in version 2.0.0: The `columns` parameter became optional.*",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.table(rows=[\n    {'make': 'Toyota', 'model': 'Celica', 'price': 35000},\n    {'make': 'Ford', 'model': 'Mondeo', 'price': 32000},\n    {'make': 'Porsche', 'model': 'Boxster', 'price': 72000},\n])\n\nui.run()",
    "url": "/documentation/table#omitting_columns"
  },
  {
    "title": "ui.table: Default column parameters",
    "content": "You can define default column parameters that apply to all columns.\nIn this example, all columns are left-aligned by default and have a blue uppercase header.\n\n*Added in version 2.0.0*",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.table(rows=[\n    {'name': 'Alice', 'age': 18},\n    {'name': 'Bob', 'age': 21},\n], columns=[\n    {'name': 'name', 'label': 'Name', 'field': 'name'},\n    {'name': 'age', 'label': 'Age', 'field': 'age'},\n], column_defaults={\n    'align': 'left',\n    'headerClasses': 'uppercase text-primary',\n})\n\nui.run()",
    "url": "/documentation/table#default_column_parameters"
  },
  {
    "title": "ui.table: Selection",
    "content": "You can set the selection type of a table using the `selection` parameter.\nThe `on_select` event handler is called when the selection changes\nand the `selected` property contains the selected rows.\n\n*Added in version 2.11.0:*\nThe `selection` property and the `set_selection` method can be used to change the selection type.",
    "format": "md",
    "demo": "from nicegui import ui\n\ntable = ui.table(\n    columns=[{'name': 'name', 'label': 'Name', 'field': 'name'}],\n    rows=[{'name': 'Alice'}, {'name': 'Bob'}, {'name': 'Charlie'}],\n    row_key='name',\n    on_select=lambda e: ui.notify(f'selected: {e.selection}'),\n)\nui.radio({None: 'none', 'single': 'single', 'multiple': 'multiple'},\n         on_change=lambda e: table.set_selection(e.value))\n\nui.run()",
    "url": "/documentation/table#selection"
  },
  {
    "title": "ui.table: Table with expandable rows",
    "content": "Scoped slots can be used to insert buttons that toggle the expand state of a table row.\nSee the [Quasar documentation](https://quasar.dev/vue-components/table#expanding-rows) for more information.",
    "format": "md",
    "demo": "from nicegui import ui\n\ncolumns = [\n    {'name': 'name', 'label': 'Name', 'field': 'name'},\n    {'name': 'age', 'label': 'Age', 'field': 'age'},\n]\nrows = [\n    {'name': 'Alice', 'age': 18},\n    {'name': 'Bob', 'age': 21},\n    {'name': 'Carol'},\n]\n\ntable = ui.table(columns=columns, rows=rows, row_key='name').classes('w-72')\ntable.add_slot('header', r'''\n    \u003Cq-tr :props=\"props\"\u003E\n        \u003Cq-th auto-width /\u003E\n        \u003Cq-th v-for=\"col in props.cols\" :key=\"col.name\" :props=\"props\"\u003E\n            {{ col.label }}\n        \u003C/q-th\u003E\n    \u003C/q-tr\u003E\n''')\ntable.add_slot('body', r'''\n    \u003Cq-tr :props=\"props\"\u003E\n        \u003Cq-td auto-width\u003E\n            \u003Cq-btn size=\"sm\" color=\"accent\" round dense\n                @click=\"props.expand = !props.expand\"\n                :icon=\"props.expand ? 'remove' : 'add'\" /\u003E\n        \u003C/q-td\u003E\n        \u003Cq-td v-for=\"col in props.cols\" :key=\"col.name\" :props=\"props\"\u003E\n            {{ col.value }}\n        \u003C/q-td\u003E\n    \u003C/q-tr\u003E\n    \u003Cq-tr v-show=\"props.expand\" :props=\"props\"\u003E\n        \u003Cq-td colspan=\"100%\"\u003E\n            \u003Cdiv class=\"text-left\"\u003EThis is {{ props.row.name }}.\u003C/div\u003E\n        \u003C/q-td\u003E\n    \u003C/q-tr\u003E\n''')\n\nui.run()",
    "url": "/documentation/table#table_with_expandable_rows"
  },
  {
    "title": "ui.table: Show and hide columns",
    "content": "Here is an example of how to show and hide columns in a table.",
    "format": "md",
    "demo": "from nicegui import ui\nfrom typing import Dict\n\ncolumns = [\n    {'name': 'name', 'label': 'Name', 'field': 'name', 'required': True, 'align': 'left'},\n    {'name': 'age', 'label': 'Age', 'field': 'age', 'sortable': True},\n]\nrows = [\n    {'name': 'Alice', 'age': 18},\n    {'name': 'Bob', 'age': 21},\n    {'name': 'Carol'},\n]\ntable = ui.table(columns=columns, rows=rows, row_key='name')\n\ndef toggle(column: Dict, visible: bool) -\u003E None:\n    column['classes'] = '' if visible else 'hidden'\n    column['headerClasses'] = '' if visible else 'hidden'\n    table.update()\n\nwith ui.button(icon='menu'):\n    with ui.menu(), ui.column().classes('gap-0 p-2'):\n        for column in columns:\n            ui.switch(column['label'], value=True, on_change=lambda e,\n                      column=column: toggle(column, e.value))\n\nui.run()",
    "url": "/documentation/table#show_and_hide_columns"
  },
  {
    "title": "ui.table: Table with drop down selection",
    "content": "Here is an example of how to use a drop down selection in a table.\nAfter emitting a `rename` event from the scoped slot, the `rename` function updates the table rows.",
    "format": "md",
    "demo": "from nicegui import events, ui\n\ncolumns = [\n    {'name': 'name', 'label': 'Name', 'field': 'name'},\n    {'name': 'age', 'label': 'Age', 'field': 'age'},\n]\nrows = [\n    {'id': 0, 'name': 'Alice', 'age': 18},\n    {'id': 1, 'name': 'Bob', 'age': 21},\n    {'id': 2, 'name': 'Carol'},\n]\nname_options = ['Alice', 'Bob', 'Carol']\n\ndef rename(e: events.GenericEventArguments) -\u003E None:\n    for row in rows:\n        if row['id'] == e.args['id']:\n            row['name'] = e.args['name']\n    ui.notify(f'Table.rows is now: {table.rows}')\n\ntable = ui.table(columns=columns, rows=rows).classes('w-full')\ntable.add_slot('body-cell-name', r'''\n    \u003Cq-td key=\"name\" :props=\"props\"\u003E\n        \u003Cq-select\n            v-model=\"props.row.name\"\n            :options=\"''' + str(name_options) + r'''\"\n            @update:model-value=\"() =\u003E $parent.$emit('rename', props.row)\"\n        /\u003E\n    \u003C/q-td\u003E\n''')\ntable.on('rename', rename)\n\nui.run()",
    "url": "/documentation/table#table_with_drop_down_selection"
  },
  {
    "title": "ui.table: Table from Pandas DataFrame",
    "content": "You can create a table from a Pandas DataFrame using the `from_pandas` method.\nThis method takes a Pandas DataFrame as input and returns a table.",
    "format": "md",
    "demo": "import pandas as pd\nfrom nicegui import ui\n\ndf = pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})\nui.table.from_pandas(df).classes('max-h-40')\n\nui.run()",
    "url": "/documentation/table#table_from_pandas_dataframe"
  },
  {
    "title": "ui.table: Table from Polars DataFrame",
    "content": "You can create a table from a Polars DataFrame using the `from_polars` method.\nThis method takes a Polars DataFrame as input and returns a table.\n\n*Added in version 2.7.0*",
    "format": "md",
    "demo": "import polars as pl\nfrom nicegui import ui\n\ndf = pl.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})\nui.table.from_polars(df).classes('max-h-40')\n\nui.run()",
    "url": "/documentation/table#table_from_polars_dataframe"
  },
  {
    "title": "ui.table: Adding rows",
    "content": "It's simple to add new rows with the `add_row(dict)` and `add_rows(list[dict])` methods.\nWith the \"virtual-scroll\" prop set, the table can be programmatically scrolled with the `scrollTo` JavaScript function.",
    "format": "md",
    "demo": "from datetime import datetime\nfrom nicegui import ui\n\ndef add():\n    table.add_row({'date': datetime.now().strftime('%c')})\n    table.run_method('scrollTo', len(table.rows)-1)\n\ncolumns = [{'name': 'date', 'label': 'Date', 'field': 'date'}]\ntable = ui.table(columns=columns, rows=[]).classes('h-52').props('virtual-scroll')\nui.button('Add row', on_click=add)\n\nui.run()",
    "url": "/documentation/table#adding_rows"
  },
  {
    "title": "ui.table: Custom sorting and formatting",
    "content": "You can define dynamic column attributes using a `:` prefix.\nThis way you can define custom sorting and formatting functions.\n\nThe following example allows sorting the `name` column by length.\nThe `age` column is formatted to show the age in years.",
    "format": "md",
    "demo": "from nicegui import ui\n\ncolumns = [\n    {\n        'name': 'name',\n        'label': 'Name',\n        'field': 'name',\n        'sortable': True,\n        ':sort': '(a, b, rowA, rowB) =\u003E b.length - a.length',\n    },\n    {\n        'name': 'age',\n        'label': 'Age',\n        'field': 'age',\n        ':format': 'value =\u003E value + \" years\"',\n    },\n]\nrows = [\n    {'name': 'Alice', 'age': 18},\n    {'name': 'Bob', 'age': 21},\n    {'name': 'Carl', 'age': 42},\n]\nui.table(columns=columns, rows=rows, row_key='name')\n\nui.run()",
    "url": "/documentation/table#custom_sorting_and_formatting"
  },
  {
    "title": "ui.table: Toggle fullscreen",
    "content": "You can toggle the fullscreen mode of a table using the `toggle_fullscreen()` method.",
    "format": "md",
    "demo": "from nicegui import ui\n\ntable = ui.table(\n    columns=[{'name': 'name', 'label': 'Name', 'field': 'name'}],\n    rows=[{'name': 'Alice'}, {'name': 'Bob'}, {'name': 'Carol'}],\n).classes('w-full')\n\nwith table.add_slot('top-left'):\n    def toggle() -\u003E None:\n        table.toggle_fullscreen()\n        button.props('icon=fullscreen_exit' if table.is_fullscreen else 'icon=fullscreen')\n    button = ui.button('Toggle fullscreen', icon='fullscreen', on_click=toggle).props('flat')\n\nui.run()",
    "url": "/documentation/table#toggle_fullscreen"
  },
  {
    "title": "ui.table: Pagination",
    "content": "You can provide either a single integer or a dictionary to define pagination.\n\nThe dictionary can contain the following keys:\n\n- `rowsPerPage`: The number of rows per page.\n- `sortBy`: The column name to sort by.\n- `descending`: Whether to sort in descending order.\n- `page`: The current page (1-based).",
    "format": "md",
    "demo": "from nicegui import ui\n\ncolumns = [\n    {'name': 'name', 'label': 'Name', 'field': 'name', 'required': True, 'align': 'left'},\n    {'name': 'age', 'label': 'Age', 'field': 'age', 'sortable': True},\n]\nrows = [\n    {'name': 'Elsa', 'age': 18},\n    {'name': 'Oaken', 'age': 46},\n    {'name': 'Hans', 'age': 20},\n    {'name': 'Sven'},\n    {'name': 'Olaf', 'age': 4},\n    {'name': 'Anna', 'age': 17},\n]\nui.table(columns=columns, rows=rows, pagination=3)\nui.table(columns=columns, rows=rows, pagination={'rowsPerPage': 4, 'sortBy': 'age', 'page': 2})\n\nui.run()",
    "url": "/documentation/table#pagination"
  },
  {
    "title": "ui.table: Handle pagination changes",
    "content": "You can handle pagination changes using the `on_pagination_change` parameter.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.table(\n    columns=[{'id': 'Name', 'label': 'Name', 'field': 'Name', 'align': 'left'}],\n    rows=[{'Name': f'Person {i}'} for i in range(100)],\n    pagination=3,\n    on_pagination_change=lambda e: ui.notify(e.value),\n)\n\nui.run()",
    "url": "/documentation/table#handle_pagination_changes"
  },
  {
    "title": "ui.table: Computed props",
    "content": "You can access the computed props of a table within async callback functions.",
    "format": "md",
    "demo": "from nicegui import ui\n\nasync def show_filtered_sorted_rows():\n    ui.notify(await table.get_filtered_sorted_rows())\n\nasync def show_computed_rows():\n    ui.notify(await table.get_computed_rows())\n\ntable = ui.table(\n    columns=[\n        {'name': 'name', 'label': 'Name', 'field': 'name', 'align': 'left', 'sortable': True},\n        {'name': 'age', 'label': 'Age', 'field': 'age', 'align': 'left', 'sortable': True}\n    ],\n    rows=[\n        {'name': 'Noah', 'age': 33},\n        {'name': 'Emma', 'age': 21},\n        {'name': 'Rose', 'age': 88},\n        {'name': 'James', 'age': 59},\n        {'name': 'Olivia', 'age': 62},\n        {'name': 'Liam', 'age': 18},\n    ],\n    row_key='name',\n    pagination=3,\n)\nui.input('Search by name/age').bind_value(table, 'filter')\nui.button('Show filtered/sorted rows', on_click=show_filtered_sorted_rows)\nui.button('Show computed rows', on_click=show_computed_rows)\n\nui.run()",
    "url": "/documentation/table#computed_props"
  },
  {
    "title": "ui.table: Computed fields",
    "content": "You can use functions to compute the value of a column.\nThe function receives the row as an argument.\nSee the [Quasar documentation](https://quasar.dev/vue-components/table#defining-the-columns) for more information.",
    "format": "md",
    "demo": "from nicegui import ui\n\ncolumns = [\n    {'name': 'name', 'label': 'Name', 'field': 'name', 'align': 'left'},\n    {'name': 'length', 'label': 'Length', ':field': 'row =\u003E row.name.length'},\n]\nrows = [\n    {'name': 'Alice'},\n    {'name': 'Bob'},\n    {'name': 'Christopher'},\n]\nui.table(columns=columns, rows=rows, row_key='name')\n\nui.run()",
    "url": "/documentation/table#computed_fields"
  },
  {
    "title": "ui.table: Conditional formatting",
    "content": "You can use scoped slots to conditionally format the content of a cell.\nSee the [Quasar documentation](https://quasar.dev/vue-components/table#example--body-cell-slot)\nfor more information about body-cell slots.\n\nIn this demo we use a `q-badge` to display the age in red if the person is under 21 years old.\nWe use the `body-cell-age` slot to insert the `q-badge` into the `age` column.\nThe \":color\" attribute of the `q-badge` is set to \"red\" if the age is under 21, otherwise it is set to \"green\".\nThe colon in front of the \"color\" attribute indicates that the value is a JavaScript expression.",
    "format": "md",
    "demo": "from nicegui import ui\n\ncolumns = [\n    {'name': 'name', 'label': 'Name', 'field': 'name'},\n    {'name': 'age', 'label': 'Age', 'field': 'age'},\n]\nrows = [\n    {'name': 'Alice', 'age': 18},\n    {'name': 'Bob', 'age': 21},\n    {'name': 'Carol', 'age': 42},\n]\ntable = ui.table(columns=columns, rows=rows, row_key='name')\ntable.add_slot('body-cell-age', '''\n    \u003Cq-td key=\"age\" :props=\"props\"\u003E\n        \u003Cq-badge :color=\"props.value \u003C 21 ? 'red' : 'green'\"\u003E\n            {{ props.value }}\n        \u003C/q-badge\u003E\n    \u003C/q-td\u003E\n''')\n\nui.run()",
    "url": "/documentation/table#conditional_formatting"
  },
  {
    "title": "ui.table: Table cells with links",
    "content": "Here is a demo of how to insert links into table cells.\nWe use the `body-cell-link` slot to insert an `\u003Ca\u003E` tag into the `link` column.",
    "format": "md",
    "demo": "from nicegui import ui\n\ncolumns = [\n    {'name': 'name', 'label': 'Name', 'field': 'name', 'align': 'left'},\n    {'name': 'link', 'label': 'Link', 'field': 'link', 'align': 'left'},\n]\nrows = [\n    {'name': 'Google', 'link': 'https://google.com'},\n    {'name': 'Facebook', 'link': 'https://facebook.com'},\n    {'name': 'Twitter', 'link': 'https://twitter.com'},\n]\ntable = ui.table(columns=columns, rows=rows, row_key='name')\ntable.add_slot('body-cell-link', '''\n    \u003Cq-td :props=\"props\"\u003E\n        \u003Ca :href=\"props.value\"\u003E{{ props.value }}\u003C/a\u003E\n    \u003C/q-td\u003E\n''')\n\nui.run()",
    "url": "/documentation/table#table_cells_with_links"
  },
  {
    "title": "ui.table: Table cells with HTML",
    "content": "This demo shows how to define a named slot to render HTML content.\nThe slot name \"body-cell-[name]\" can be adjusted to match any column with corresponding name.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.table(rows=[\n    {'name': 'bold', 'code': '\u003Cb\u003EBold\u003C/b\u003E'},\n    {'name': 'italic', 'code': '\u003Ci\u003EItalic\u003C/i\u003E'},\n    {'name': 'underline', 'code': '\u003Cu\u003EUnderline\u003C/u\u003E'},\n]).add_slot('body-cell-code', '\u003Cq-td v-html=\"props.row.code\"\u003E\u003C/q-td\u003E')\n\nui.run()",
    "url": "/documentation/table#table_cells_with_html"
  },
  {
    "title": "ui.table: Table with masonry-like grid",
    "content": "You can use the `grid` prop to display the table as a masonry-like grid.\nSee the [Quasar documentation](https://quasar.dev/vue-components/table#grid-style) for more information.",
    "format": "md",
    "demo": "from nicegui import ui\n\ncolumns = [\n    {'name': 'name', 'label': 'Name', 'field': 'name'},\n    {'name': 'age', 'label': 'Age', 'field': 'age'},\n]\nrows = [\n    {'name': 'Alice', 'age': 18},\n    {'name': 'Bob', 'age': 21},\n    {'name': 'Carol', 'age': 42},\n]\ntable = ui.table(columns=columns, rows=rows, row_key='name').props('grid')\ntable.add_slot('item', r'''\n    \u003Cq-card flat bordered :props=\"props\" class=\"m-1\"\u003E\n        \u003Cq-card-section class=\"text-center\"\u003E\n            \u003Cstrong\u003E{{ props.row.name }}\u003C/strong\u003E\n        \u003C/q-card-section\u003E\n        \u003Cq-separator /\u003E\n        \u003Cq-card-section class=\"text-center\"\u003E\n            \u003Cdiv\u003E{{ props.row.age }} years\u003C/div\u003E\n        \u003C/q-card-section\u003E\n    \u003C/q-card\u003E\n''')\n\nui.run()",
    "url": "/documentation/table#table_with_masonry-like_grid"
  },
  {
    "title": "ui.table: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/table#reference"
  },
  {
    "title": "ui.tree: Tree",
    "content": "Display hierarchical data using Quasar's `QTree \u003Chttps://quasar.dev/vue-components/tree\u003E`_ component.\n\nIf using IDs, make sure they are unique within the whole tree.\n\nTo use checkboxes and ``on_tick``, set the ``tick_strategy`` parameter to \"leaf\", \"leaf-filtered\" or \"strict\".\n\n:param nodes: hierarchical list of node objects\n:param node_key: property name of each node object that holds its unique id (default: \"id\")\n:param label_key: property name of each node object that holds its label (default: \"label\")\n:param children_key: property name of each node object that holds its list of children (default: \"children\")\n:param on_select: callback which is invoked when the node selection changes\n:param on_expand: callback which is invoked when the node expansion changes\n:param on_tick: callback which is invoked when a node is ticked or unticked\n:param tick_strategy: whether and how to use checkboxes (\"leaf\", \"leaf-filtered\" or \"strict\"; default: ``None``)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.tree([\n    {'id': 'numbers', 'children': [{'id': '1'}, {'id': '2'}]},\n    {'id': 'letters', 'children': [{'id': 'A'}, {'id': 'B'}]},\n], label_key='id', on_select=lambda e: ui.notify(e.value))\n\nui.run()",
    "url": "/documentation/tree#tree"
  },
  {
    "title": "ui.tree: Tree with custom header and body",
    "content": "Scoped slots can be used to insert custom content into the header and body of a tree node.\nSee the [Quasar documentation](https://quasar.dev/vue-components/tree#customize-content) for more information.",
    "format": "md",
    "demo": "from nicegui import ui\n\ntree = ui.tree([\n    {'id': 'numbers', 'description': 'Just some numbers', 'children': [\n        {'id': '1', 'description': 'The first number'},\n        {'id': '2', 'description': 'The second number'},\n    ]},\n    {'id': 'letters', 'description': 'Some latin letters', 'children': [\n        {'id': 'A', 'description': 'The first letter'},\n        {'id': 'B', 'description': 'The second letter'},\n    ]},\n], label_key='id', on_select=lambda e: ui.notify(e.value))\n\ntree.add_slot('default-header', '''\n    \u003Cspan :props=\"props\"\u003ENode \u003Cstrong\u003E{{ props.node.id }}\u003C/strong\u003E\u003C/span\u003E\n''')\ntree.add_slot('default-body', '''\n    \u003Cspan :props=\"props\"\u003EDescription: \"{{ props.node.description }}\"\u003C/span\u003E\n''')\n\nui.run()",
    "url": "/documentation/tree#tree_with_custom_header_and_body"
  },
  {
    "title": "ui.tree: Tree with checkboxes",
    "content": "The tree can be used with checkboxes by setting the \"tick-strategy\" prop.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.tree([\n    {'id': 'A', 'children': [{'id': 'A1'}, {'id': 'A2'}]},\n    {'id': 'B', 'children': [{'id': 'B1'}, {'id': 'B2'}]},\n], label_key='id', tick_strategy='leaf', on_tick=lambda e: ui.notify(e.value))\n\nui.run()",
    "url": "/documentation/tree#tree_with_checkboxes"
  },
  {
    "title": "ui.tree: Expand/collapse programmatically",
    "content": "The whole tree or individual nodes can be toggled programmatically using the `expand()` and `collapse()` methods.\nThis even works if a node is disabled (e.g. not clickable by the user).",
    "format": "md",
    "demo": "from nicegui import ui\n\nt = ui.tree([\n    {'id': 'A', 'children': [{'id': 'A1'}, {'id': 'A2'}], 'disabled': True},\n    {'id': 'B', 'children': [{'id': 'B1'}, {'id': 'B2'}]},\n], label_key='id').expand()\n\nwith ui.row():\n    ui.button('+ all', on_click=t.expand)\n    ui.button('- all', on_click=t.collapse)\n    ui.button('+ A', on_click=lambda: t.expand(['A']))\n    ui.button('- A', on_click=lambda: t.collapse(['A']))\n\nui.run()",
    "url": "/documentation/tree#expand_collapse_programmatically"
  },
  {
    "title": "ui.tree: Select/deselect programmatically",
    "content": "You can select or deselect nodes with the `select()` and `deselect()` methods.",
    "format": "md",
    "demo": "from nicegui import ui\n\nt = ui.tree([\n    {'id': 'numbers', 'children': [{'id': '1'}, {'id': '2'}]},\n    {'id': 'letters', 'children': [{'id': 'A'}, {'id': 'B'}]},\n], label_key='id').expand()\n\nwith ui.row():\n    ui.button('Select A', on_click=lambda: t.select('A'))\n    ui.button('Deselect A', on_click=t.deselect)\n\nui.run()",
    "url": "/documentation/tree#select_deselect_programmatically"
  },
  {
    "title": "ui.tree: Tick/untick programmatically",
    "content": "After setting a `tick_strategy`, you can tick or untick nodes with the `tick()` and `untick()` methods.\nYou can either specify a list of node keys or `None` to tick or untick all nodes.",
    "format": "md",
    "demo": "from nicegui import ui\n\nt = ui.tree([\n    {'id': 'numbers', 'children': [{'id': '1'}, {'id': '2'}]},\n    {'id': 'letters', 'children': [{'id': 'A'}, {'id': 'B'}]},\n], label_key='id', tick_strategy='leaf').expand()\n\nwith ui.row():\n    ui.button('Tick 1, 2 and B', on_click=lambda: t.tick(['1', '2', 'B']))\n    ui.button('Untick 2 and B', on_click=lambda: t.untick(['2', 'B']))\nwith ui.row():\n    ui.button('Tick all', on_click=t.tick)\n    ui.button('Untick all', on_click=t.untick)\n\nui.run()",
    "url": "/documentation/tree#tick_untick_programmatically"
  },
  {
    "title": "ui.tree: Filter nodes",
    "content": "You can filter nodes by setting the `filter` property.\nThe tree will only show nodes that match the filter.",
    "format": "md",
    "demo": "from nicegui import ui\n\nt = ui.tree([\n    {'id': 'fruits', 'children': [{'id': 'Apple'}, {'id': 'Banana'}]},\n    {'id': 'vegetables', 'children': [{'id': 'Potato'}, {'id': 'Tomato'}]},\n], label_key='id').expand()\nui.input('filter').bind_value_to(t, 'filter')\n\nui.run()",
    "url": "/documentation/tree#filter_nodes"
  },
  {
    "title": "ui.tree: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/tree#reference"
  },
  {
    "title": "Data Elements: Table",
    "content": "A table based on Quasar's `QTable \u003Chttps://quasar.dev/vue-components/table\u003E`_ component.\n\n:param rows: list of row objects\n:param columns: list of column objects (defaults to the columns of the first row *since version 2.0.0*)\n:param column_defaults: optional default column properties, *added in version 2.0.0*\n:param row_key: name of the column containing unique data identifying the row (default: \"id\")\n:param title: title of the table\n:param selection: selection type (\"single\" or \"multiple\"; default: `None`)\n:param pagination: a dictionary correlating to a pagination object or number of rows per page (`None` hides the pagination, 0 means \"infinite\"; default: `None`).\n:param on_select: callback which is invoked when the selection changes\n:param on_pagination_change: callback which is invoked when the pagination changes\n\nIf selection is 'single' or 'multiple', then a `selected` property is accessible containing the selected rows.\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\ncolumns = [\n    {'name': 'name', 'label': 'Name', 'field': 'name', 'required': True, 'align': 'left'},\n    {'name': 'age', 'label': 'Age', 'field': 'age', 'sortable': True},\n]\nrows = [\n    {'name': 'Alice', 'age': 18},\n    {'name': 'Bob', 'age': 21},\n    {'name': 'Carol'},\n]\nui.table(columns=columns, rows=rows, row_key='name')\n\nui.run()",
    "url": "/documentation/section_data_elements#table"
  },
  {
    "title": "Data Elements: AG Grid",
    "content": "An element to create a grid using `AG Grid \u003Chttps://www.ag-grid.com/\u003E`_.\n\nThe methods ``run_grid_method`` and ``run_row_method`` can be used to interact with the AG Grid instance on the client.\n\n:param options: dictionary of AG Grid options\n:param html_columns: list of columns that should be rendered as HTML (default: ``[]``)\n:param theme: AG Grid theme (default: \"balham\")\n:param auto_size_columns: whether to automatically resize columns to fit the grid width (default: ``True``)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\ngrid = ui.aggrid({\n    'defaultColDef': {'flex': 1},\n    'columnDefs': [\n        {'headerName': 'Name', 'field': 'name'},\n        {'headerName': 'Age', 'field': 'age'},\n        {'headerName': 'Parent', 'field': 'parent', 'hide': True},\n    ],\n    'rowData': [\n        {'name': 'Alice', 'age': 18, 'parent': 'David'},\n        {'name': 'Bob', 'age': 21, 'parent': 'Eve'},\n        {'name': 'Carol', 'age': 42, 'parent': 'Frank'},\n    ],\n    'rowSelection': 'multiple',\n}).classes('max-h-40')\n\ndef update():\n    grid.options['rowData'][0]['age'] += 1\n    grid.update()\n\nui.button('Update', on_click=update)\nui.button('Select all', on_click=lambda: grid.run_grid_method('selectAll'))\nui.button('Show parent', on_click=lambda: grid.run_grid_method('setColumnsVisible', ['parent'], True))\n\nui.run()",
    "url": "/documentation/section_data_elements#ag_grid"
  },
  {
    "title": "Data Elements: Highcharts chart",
    "content": "An element to create a chart using `Highcharts \u003Chttps://www.highcharts.com/\u003E`_.\nUpdates can be pushed to the chart by changing the `options` property.\nAfter data has changed, call the `update` method to refresh the chart.\n\nDue to Highcharts' restrictive license, this element is not part of the standard NiceGUI package.\nIt is maintained in a `separate repository \u003Chttps://github.com/zauberzeug/nicegui-highcharts/\u003E`_\nand can be installed with `pip install nicegui[highcharts]`.\n\nBy default, a `Highcharts.chart` is created.\nTo use, e.g., `Highcharts.stockChart` instead, set the `type` property to \"stockChart\".\n\n:param options: dictionary of Highcharts options\n:param type: chart type (e.g. \"chart\", \"stockChart\", \"mapChart\", ...; default: \"chart\")\n:param extras: list of extra dependencies to include (e.g. \"annotations\", \"arc-diagram\", \"solid-gauge\", ...)\n:param on_point_click: callback function that is called when a point is clicked\n:param on_point_drag_start: callback function that is called when a point drag starts\n:param on_point_drag: callback function that is called when a point is dragged\n:param on_point_drop: callback function that is called when a point is dropped\n",
    "format": "rst",
    "demo": "from nicegui import ui\nfrom random import random\n\nchart = ui.highchart({\n    'title': False,\n    'chart': {'type': 'bar'},\n    'xAxis': {'categories': ['A', 'B']},\n    'series': [\n        {'name': 'Alpha', 'data': [0.1, 0.2]},\n        {'name': 'Beta', 'data': [0.3, 0.4]},\n    ],\n}).classes('w-full h-64')\n\ndef update():\n    chart.options['series'][0]['data'][0] = random()\n    chart.update()\n\nui.button('Update', on_click=update)\n\nui.run()",
    "url": "/documentation/section_data_elements#highcharts_chart"
  },
  {
    "title": "Data Elements: Apache EChart",
    "content": "An element to create a chart using `ECharts \u003Chttps://echarts.apache.org/\u003E`_.\nUpdates can be pushed to the chart by changing the `options` property.\nAfter data has changed, call the `update` method to refresh the chart.\n\n:param options: dictionary of EChart options\n:param on_click_point: callback that is invoked when a point is clicked\n:param enable_3d: enforce importing the echarts-gl library\n:param renderer: renderer to use (\"canvas\" or \"svg\", *added in version 2.7.0*)\n:param theme: an EChart theme configuration (dictionary or a URL returning a JSON object, *added in version 2.15.0*)\n",
    "format": "rst",
    "demo": "from nicegui import ui\nfrom random import random\n\nechart = ui.echart({\n    'xAxis': {'type': 'value'},\n    'yAxis': {'type': 'category', 'data': ['A', 'B'], 'inverse': True},\n    'legend': {'textStyle': {'color': 'gray'}},\n    'series': [\n        {'type': 'bar', 'name': 'Alpha', 'data': [0.1, 0.2]},\n        {'type': 'bar', 'name': 'Beta', 'data': [0.3, 0.4]},\n    ],\n})\n\ndef update():\n    echart.options['series'][0]['data'][0] = random()\n    echart.update()\n\nui.button('Update', on_click=update)\n\nui.run()",
    "url": "/documentation/section_data_elements#apache_echart"
  },
  {
    "title": "Data Elements: Pyplot Context",
    "content": "Create a context to configure a `Matplotlib \u003Chttps://matplotlib.org/\u003E`_ plot.\n\n:param close: whether the figure should be closed after exiting the context; set to `False` if you want to update it later (default: `True`)\n:param kwargs: arguments like `figsize` which should be passed to `pyplot.figure \u003Chttps://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.figure.html\u003E`_\n",
    "format": "rst",
    "demo": "import numpy as np\nfrom matplotlib import pyplot as plt\nfrom nicegui import ui\n\nwith ui.pyplot(figsize=(3, 2)):\n    x = np.linspace(0.0, 5.0)\n    y = np.cos(2 * np.pi * x) * np.exp(-x)\n    plt.plot(x, y, '-')\n\nui.run()",
    "url": "/documentation/section_data_elements#pyplot_context"
  },
  {
    "title": "Data Elements: Matplotlib",
    "content": "Create a `Matplotlib \u003Chttps://matplotlib.org/\u003E`_ element rendering a Matplotlib figure.\nThe figure is automatically updated when leaving the figure context.\n\n:param kwargs: arguments like `figsize` which should be passed to `matplotlib.figure.Figure \u003Chttps://matplotlib.org/stable/api/figure_api.html#matplotlib.figure.Figure\u003E`_\n",
    "format": "rst",
    "demo": "import numpy as np\nfrom nicegui import ui\n\nwith ui.matplotlib(figsize=(3, 2)).figure as fig:\n    x = np.linspace(0.0, 5.0)\n    y = np.cos(2 * np.pi * x) * np.exp(-x)\n    ax = fig.gca()\n    ax.plot(x, y, '-')\n\nui.run()",
    "url": "/documentation/section_data_elements#matplotlib"
  },
  {
    "title": "Data Elements: Line Plot",
    "content": "Create a line plot using pyplot.\nThe `push` method provides live updating when utilized in combination with `ui.timer`.\n\n:param n: number of lines\n:param limit: maximum number of datapoints per line (new points will displace the oldest)\n:param update_every: update plot only after pushing new data multiple times to save CPU and bandwidth\n:param close: whether the figure should be closed after exiting the context; set to `False` if you want to update it later (default: `True`)\n:param kwargs: arguments like `figsize` which should be passed to `pyplot.figure \u003Chttps://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.figure.html\u003E`_\n",
    "format": "rst",
    "demo": "import math\nfrom datetime import datetime\nfrom nicegui import ui\n\nline_plot = ui.line_plot(n=2, limit=20, figsize=(3, 2), update_every=5) \\\n    .with_legend(['sin', 'cos'], loc='upper center', ncol=2)\n\ndef update_line_plot() -\u003E None:\n    now = datetime.now()\n    x = now.timestamp()\n    y1 = math.sin(x)\n    y2 = math.cos(x)\n    line_plot.push([now], [[y1], [y2]], y_limits=(-1.5, 1.5))\n\nline_updates = ui.timer(0.1, update_line_plot, active=False)\nline_checkbox = ui.checkbox('active').bind_value(line_updates, 'active')\n\nui.run()",
    "url": "/documentation/section_data_elements#line_plot"
  },
  {
    "title": "Data Elements: Plotly Element",
    "content": "Renders a Plotly chart.\nThere are two ways to pass a Plotly figure for rendering, see parameter `figure`:\n\n* Pass a `go.Figure` object, see https://plotly.com/python/\n\n* Pass a Python `dict` object with keys `data`, `layout`, `config` (optional), see https://plotly.com/javascript/\n\nFor best performance, use the declarative `dict` approach for creating a Plotly chart.\n\n:param figure: Plotly figure to be rendered. Can be either a `go.Figure` instance, or\n               a `dict` object with keys `data`, `layout`, `config` (optional).\n",
    "format": "rst",
    "demo": "import plotly.graph_objects as go\nfrom nicegui import ui\n\nfig = go.Figure(go.Scatter(x=[1, 2, 3, 4], y=[1, 2, 3, 2.5]))\nfig.update_layout(margin=dict(l=0, r=0, t=0, b=0))\nui.plotly(fig).classes('w-full h-40')\n\nui.run()",
    "url": "/documentation/section_data_elements#plotly_element"
  },
  {
    "title": "Data Elements: Linear Progress",
    "content": "A linear progress bar wrapping Quasar's\n`QLinearProgress \u003Chttps://quasar.dev/vue-components/linear-progress\u003E`_ component.\n\n:param value: the initial value of the field (from 0.0 to 1.0)\n:param size: the height of the progress bar (default: \"20px\" with value label and \"4px\" without)\n:param show_value: whether to show a value label in the center (default: `True`)\n:param color: color (either a Quasar, Tailwind, or CSS color or `None`, default: \"primary\")\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nslider = ui.slider(min=0, max=1, step=0.01, value=0.5)\nui.linear_progress().bind_value_from(slider, 'value')\n\nui.run()",
    "url": "/documentation/section_data_elements#linear_progress"
  },
  {
    "title": "Data Elements: Circular Progress",
    "content": "A circular progress bar wrapping Quasar's\n`QCircularProgress \u003Chttps://quasar.dev/vue-components/circular-progress\u003E`_.\n\n:param value: the initial value of the field\n:param min: the minimum value (default: 0.0)\n:param max: the maximum value (default: 1.0)\n:param size: the size of the progress circle (default: \"xl\")\n:param show_value: whether to show a value label in the center (default: `True`)\n:param color: color (either a Quasar, Tailwind, or CSS color or `None`, default: \"primary\")\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nslider = ui.slider(min=0, max=1, step=0.01, value=0.5)\nui.circular_progress().bind_value_from(slider, 'value')\n\nui.run()",
    "url": "/documentation/section_data_elements#circular_progress"
  },
  {
    "title": "Data Elements: Spinner",
    "content": "This element is based on Quasar's `QSpinner \u003Chttps://quasar.dev/vue-components/spinners\u003E`_ component.\n\n:param type: type of spinner (e.g. \"audio\", \"ball\", \"bars\", ..., default: \"default\")\n:param size: size of the spinner (e.g. \"3em\", \"10px\", \"xl\", ..., default: \"1em\")\n:param color: color of the spinner (either a Quasar, Tailwind, or CSS color or `None`, default: \"primary\")\n:param thickness: thickness of the spinner (applies to the \"default\" spinner only, default: 5.0)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.row():\n    ui.spinner(size='lg')\n    ui.spinner('audio', size='lg', color='green')\n    ui.spinner('dots', size='lg', color='red')\n\nui.run()",
    "url": "/documentation/section_data_elements#spinner"
  },
  {
    "title": "Data Elements: 3D Scene",
    "content": "Display a 3D scene using `three.js \u003Chttps://threejs.org/\u003E`_.\nCurrently NiceGUI supports boxes, spheres, cylinders/cones, extrusions, straight lines, curves and textured meshes.\nObjects can be translated, rotated and displayed with different color, opacity or as wireframes.\nThey can also be grouped to apply joint movements.\n\n:param width: width of the canvas\n:param height: height of the canvas\n:param grid: whether to display a grid (boolean or tuple of ``size`` and ``divisions`` for `Three.js' GridHelper \u003Chttps://threejs.org/docs/#api/en/helpers/GridHelper\u003E`_, default: 100x100)\n:param camera: camera definition, either instance of ``ui.scene.perspective_camera`` (default) or ``ui.scene.orthographic_camera``\n:param on_click: callback to execute when a 3D object is clicked (use ``click_events`` to specify which events to subscribe to)\n:param click_events: list of JavaScript click events to subscribe to (default: ``['click', 'dblclick']``)\n:param on_drag_start: callback to execute when a 3D object is dragged\n:param on_drag_end: callback to execute when a 3D object is dropped\n:param drag_constraints: comma-separated JavaScript expression for constraining positions of dragged objects (e.g. ``'x = 0, z = y / 2'``)\n:param background_color: background color of the scene (default: \"#eee\")\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.scene().classes('w-full h-64') as scene:\n    scene.axes_helper()\n    scene.sphere().material('#4488ff').move(2, 2)\n    scene.cylinder(1, 0.5, 2, 20).material('#ff8800', opacity=0.5).move(-2, 1)\n    scene.extrusion([[0, 0], [0, 1], [1, 0.5]], 0.1).material('#ff8888').move(2, -1)\n\n    with scene.group().move(z=2):\n        scene.box().move(x=2)\n        scene.box().move(y=2).rotate(0.25, 0.5, 0.75)\n        scene.box(wireframe=True).material('#888888').move(x=2, y=2)\n\n    scene.line([-4, 0, 0], [-4, 2, 0]).material('#ff0000')\n    scene.curve([-4, 0, 0], [-4, -1, 0], [-3, -1, 0], [-3, 0, 0]).material('#008800')\n\n    logo = 'https://avatars.githubusercontent.com/u/2843826'\n    scene.texture(logo, [[[0.5, 2, 0], [2.5, 2, 0]],\n                         [[0.5, 0, 0], [2.5, 0, 0]]]).move(1, -3)\n\n    teapot = 'https://upload.wikimedia.org/wikipedia/commons/9/93/Utah_teapot_(solid).stl'\n    scene.stl(teapot).scale(0.2).move(-3, 4)\n\n    avocado = 'https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Assets/main/Models/Avocado/glTF-Binary/Avocado.glb'\n    scene.gltf(avocado).scale(40).move(-2, -3, 0.5)\n\n    scene.text('2D', 'background: rgba(0, 0, 0, 0.2); border-radius: 5px; padding: 5px').move(z=2)\n    scene.text3d('3D', 'background: rgba(0, 0, 0, 0.2); border-radius: 5px; padding: 5px').move(y=-2).scale(.05)\n\nui.run()",
    "url": "/documentation/section_data_elements#3d_scene"
  },
  {
    "title": "Data Elements: Leaflet map",
    "content": "This element is a wrapper around the `Leaflet \u003Chttps://leafletjs.com/\u003E`_ JavaScript library.\n\n:param center: initial center location of the map (latitude/longitude, default: (0.0, 0.0))\n:param zoom: initial zoom level of the map (default: 13)\n:param draw_control: whether to show the draw toolbar (default: False)\n:param options: additional options passed to the Leaflet map (default: {})\n:param hide_drawn_items: whether to hide drawn items on the map (default: False, *added in version 2.0.0*)\n:param additional_resources: additional resources like CSS or JS files to load (default: None, *added in version 2.11.0*)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nm = ui.leaflet(center=(51.505, -0.09))\nui.label().bind_text_from(m, 'center', lambda center: f'Center: {center[0]:.3f}, {center[1]:.3f}')\nui.label().bind_text_from(m, 'zoom', lambda zoom: f'Zoom: {zoom}')\n\nwith ui.grid(columns=2):\n    ui.button('London', on_click=lambda: m.set_center((51.505, -0.090)))\n    ui.button('Berlin', on_click=lambda: m.set_center((52.520, 13.405)))\n    ui.button(icon='zoom_in', on_click=lambda: m.set_zoom(m.zoom + 1))\n    ui.button(icon='zoom_out', on_click=lambda: m.set_zoom(m.zoom - 1))\n\nui.run()",
    "url": "/documentation/section_data_elements#leaflet_map"
  },
  {
    "title": "Data Elements: Tree",
    "content": "Display hierarchical data using Quasar's `QTree \u003Chttps://quasar.dev/vue-components/tree\u003E`_ component.\n\nIf using IDs, make sure they are unique within the whole tree.\n\nTo use checkboxes and ``on_tick``, set the ``tick_strategy`` parameter to \"leaf\", \"leaf-filtered\" or \"strict\".\n\n:param nodes: hierarchical list of node objects\n:param node_key: property name of each node object that holds its unique id (default: \"id\")\n:param label_key: property name of each node object that holds its label (default: \"label\")\n:param children_key: property name of each node object that holds its list of children (default: \"children\")\n:param on_select: callback which is invoked when the node selection changes\n:param on_expand: callback which is invoked when the node expansion changes\n:param on_tick: callback which is invoked when a node is ticked or unticked\n:param tick_strategy: whether and how to use checkboxes (\"leaf\", \"leaf-filtered\" or \"strict\"; default: ``None``)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.tree([\n    {'id': 'numbers', 'children': [{'id': '1'}, {'id': '2'}]},\n    {'id': 'letters', 'children': [{'id': 'A'}, {'id': 'B'}]},\n], label_key='id', on_select=lambda e: ui.notify(e.value))\n\nui.run()",
    "url": "/documentation/section_data_elements#tree"
  },
  {
    "title": "Data Elements: Log View",
    "content": "Create a log view that allows to add new lines without re-transmitting the whole history to the client.\n\n:param max_lines: maximum number of lines before dropping oldest ones (default: `None`)\n",
    "format": "rst",
    "demo": "from datetime import datetime\nfrom nicegui import ui\n\nlog = ui.log(max_lines=10).classes('w-full h-20')\nui.button('Log time', on_click=lambda: log.push(datetime.now().strftime('%X.%f')[:-5]))\n\nui.run()",
    "url": "/documentation/section_data_elements#log_view"
  },
  {
    "title": "Data Elements: Editor",
    "content": "A WYSIWYG editor based on `Quasar's QEditor \u003Chttps://quasar.dev/vue-components/editor\u003E`_.\nThe value is a string containing the formatted text as HTML code.\n\n:param value: initial value\n:param on_change: callback to be invoked when the value changes\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\neditor = ui.editor(placeholder='Type something here')\nui.markdown().bind_content_from(editor, 'value',\n                                backward=lambda v: f'HTML code:\\n```\\n{v}\\n```')\n\nui.run()",
    "url": "/documentation/section_data_elements#editor"
  },
  {
    "title": "Data Elements: Code",
    "content": "This element displays a code block with syntax highlighting.\n\nIn secure environments (HTTPS or localhost), a copy button is displayed to copy the code to the clipboard.\n\n:param content: code to display\n:param language: language of the code (default: \"python\")\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.code('''\n    from nicegui import ui\n\n    ui.label('Code inception!')\n\n    ui.run()\n''').classes('w-full')\n\nui.run()",
    "url": "/documentation/section_data_elements#code"
  },
  {
    "title": "Data Elements: JSONEditor",
    "content": "An element to create a JSON editor using `JSONEditor \u003Chttps://github.com/josdejong/svelte-jsoneditor\u003E`_.\nUpdates can be pushed to the editor by changing the `properties` property.\nAfter data has changed, call the `update` method to refresh the editor.\n\n:param properties: dictionary of JSONEditor properties\n:param on_select: callback which is invoked when some of the content has been selected\n:param on_change: callback which is invoked when the content has changed\n:param schema: optional `JSON schema \u003Chttps://json-schema.org/\u003E`_ for validating the data being edited (*added in version 2.8.0*)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\njson = {\n    'array': [1, 2, 3],\n    'boolean': True,\n    'color': '#82b92c',\n    None: None,\n    'number': 123,\n    'object': {\n        'a': 'b',\n        'c': 'd',\n    },\n    'time': 1575599819000,\n    'string': 'Hello World',\n}\nui.json_editor({'content': {'json': json}},\n               on_select=lambda e: ui.notify(f'Select: {e}'),\n               on_change=lambda e: ui.notify(f'Change: {e}'))\n\nui.run()",
    "url": "/documentation/section_data_elements#jsoneditor"
  },
  {
    "title": "ui.card: Card",
    "content": "This element is based on Quasar's `QCard \u003Chttps://quasar.dev/vue-components/card\u003E`_ component.\nIt provides a container with a dropped shadow.\n\nNote:\nIn contrast to this element,\nthe original QCard has no padding by default and hides outer borders and shadows of nested elements.\nIf you want the original behavior, use the `tight` method.\n\n*Updated in version 2.0.0: Don't hide outer borders and shadows of nested elements anymore.*\n\n:param align_items: alignment of the items in the card (\"start\", \"end\", \"center\", \"baseline\", or \"stretch\"; default: `None`)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.card().tight():\n    ui.image('https://picsum.photos/id/684/640/360')\n    with ui.card_section():\n        ui.label('Lorem ipsum dolor sit amet, consectetur adipiscing elit, ...')\n\nui.run()",
    "url": "/documentation/card#card"
  },
  {
    "title": "ui.card: Card without shadow",
    "content": "You can remove the shadow from a card by adding the `no-shadow` class.\nThe following demo shows a 1 pixel wide border instead.\n\nAlternatively, you can use Quasar's \"flat\" and \"bordered\" props to achieve the same effect.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.card().classes('no-shadow border-[1px]'):\n    ui.label('See, no shadow!')\n\nwith ui.card().props('flat bordered'):\n    ui.label('Also no shadow!')\n\nui.run()",
    "url": "/documentation/card#card_without_shadow"
  },
  {
    "title": "ui.card: Tight card layout",
    "content": "By default, cards have a padding.\nYou can remove the padding and gaps between nested elements by using the `tight` method.\nThis also hides outer borders and shadows of nested elements, like in an original QCard.",
    "format": "md",
    "demo": "from nicegui import ui\n\nrows = [{'age': '16'}, {'age': '18'}, {'age': '21'}]\n\nwith ui.row():\n    with ui.card():\n        ui.table(rows=rows).props('flat bordered')\n\n    with ui.card().tight():\n        ui.table(rows=rows).props('flat bordered')\n\nui.run()",
    "url": "/documentation/card#tight_card_layout"
  },
  {
    "title": "ui.card: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/card#reference"
  },
  {
    "title": "ui.carousel: Carousel",
    "content": "This element represents `Quasar's QCarousel \u003Chttps://quasar.dev/vue-components/carousel#qcarousel-api\u003E`_ component.\nIt contains individual carousel slides.\n\n:param value: `ui.carousel_slide` or name of the slide to be initially selected (default: `None` meaning the first slide)\n:param on_value_change: callback to be executed when the selected slide changes\n:param animated: whether to animate slide transitions (default: `False`)\n:param arrows: whether to show arrows for manual slide navigation (default: `False`)\n:param navigation: whether to show navigation dots for manual slide navigation (default: `False`)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.carousel(animated=True, arrows=True, navigation=True).props('height=180px'):\n    with ui.carousel_slide().classes('p-0'):\n        ui.image('https://picsum.photos/id/30/270/180').classes('w-[270px]')\n    with ui.carousel_slide().classes('p-0'):\n        ui.image('https://picsum.photos/id/31/270/180').classes('w-[270px]')\n    with ui.carousel_slide().classes('p-0'):\n        ui.image('https://picsum.photos/id/32/270/180').classes('w-[270px]')\n\nui.run()",
    "url": "/documentation/carousel#carousel"
  },
  {
    "title": "ui.carousel: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/carousel#reference"
  },
  {
    "title": "ui.column: Column Element",
    "content": "Provides a container which arranges its child in a column.\n\n:param wrap: whether to wrap the content (default: `False`)\n:param align_items: alignment of the items in the column (\"start\", \"end\", \"center\", \"baseline\", or \"stretch\"; default: `None`)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.column():\n    ui.label('label 1')\n    ui.label('label 2')\n    ui.label('label 3')\n\nui.run()",
    "url": "/documentation/column#column_element"
  },
  {
    "title": "ui.column: Masonry or Pinterest-Style Layout",
    "content": "To create a masonry/Pinterest layout, the normal `ui.column` can not be used.\nBut it can be achieved with a few TailwindCSS classes.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.element('div').classes('columns-3 w-full gap-2'):\n    for i, height in enumerate([50, 50, 50, 150, 100, 50]):\n        tailwind = f'mb-2 p-2 h-[{height}px] bg-blue-100 break-inside-avoid'\n        with ui.card().classes(tailwind):\n            ui.label(f'Card #{i+1}')\n\nui.run()",
    "url": "/documentation/column#masonry_or_pinterest-style_layout"
  },
  {
    "title": "ui.column: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/column#reference"
  },
  {
    "title": "ui.context_menu: Context Menu",
    "content": "Creates a context menu based on Quasar's `QMenu \u003Chttps://quasar.dev/vue-components/menu\u003E`_ component.\nThe context menu should be placed inside the element where it should be shown.\nIt is automatically opened when the user right-clicks on the element and appears at the mouse position.\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.image('https://picsum.photos/id/377/640/360'):\n    with ui.context_menu():\n        ui.menu_item('Flip horizontally')\n        ui.menu_item('Flip vertically')\n        ui.separator()\n        ui.menu_item('Reset', auto_close=False)\n\nui.run()",
    "url": "/documentation/context_menu#context_menu"
  },
  {
    "title": "ui.context_menu: Context menus with dynamic content",
    "content": "To show a context menu with content that changes dynamically, e.g. based on the position of the mouse,\nit is recommended to re-use the same context menu instance.\nThis demo shows how to clear the context menu and add new items to it.",
    "format": "md",
    "demo": "from nicegui import events, ui\n\ndef update_menu(e: events.MouseEventArguments) -\u003E None:\n    context_menu.clear()\n    with context_menu:\n        ui.menu_item(f'Add circle at ({e.image_x:.0f}, {e.image_y:.0f})')\n\nsource = 'https://picsum.photos/id/377/640/360'\nwith ui.interactive_image(source, on_mouse=update_menu, events=['contextmenu']):\n    context_menu = ui.context_menu()\n\nui.run()",
    "url": "/documentation/context_menu#context_menus_with_dynamic_content"
  },
  {
    "title": "ui.context_menu: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/context_menu#reference"
  },
  {
    "title": "ui.dialog: Dialog",
    "content": "Creates a dialog based on Quasar's `QDialog \u003Chttps://quasar.dev/vue-components/dialog\u003E`_ component.\nBy default it is dismissible by clicking or pressing ESC.\nTo make it persistent, set `.props('persistent')` on the dialog element.\n\nNOTE: The dialog is an element.\nThat means it is not removed when closed, but only hidden.\nYou should either create it only once and then reuse it, or remove it with `.clear()` after dismissal.\n\n:param value: whether the dialog should be opened on creation (default: `False`)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.dialog() as dialog, ui.card():\n    ui.label('Hello world!')\n    ui.button('Close', on_click=dialog.close)\n\nui.button('Open a dialog', on_click=dialog.open)\n\nui.run()",
    "url": "/documentation/dialog#dialog"
  },
  {
    "title": "ui.dialog: Awaitable dialog",
    "content": "Dialogs can be awaited.\nUse the `submit` method to close the dialog and return a result.\nCanceling the dialog by clicking in the background or pressing the escape key yields `None`.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.dialog() as dialog, ui.card():\n    ui.label('Are you sure?')\n    with ui.row():\n        ui.button('Yes', on_click=lambda: dialog.submit('Yes'))\n        ui.button('No', on_click=lambda: dialog.submit('No'))\n\nasync def show():\n    result = await dialog\n    ui.notify(f'You chose {result}')\n\nui.button('Await a dialog', on_click=show)\n\nui.run()",
    "url": "/documentation/dialog#awaitable_dialog"
  },
  {
    "title": "ui.dialog: Replacing content",
    "content": "The content of a dialog can be changed.",
    "format": "md",
    "demo": "from nicegui import ui\n\ndef replace():\n    dialog.clear()\n    with dialog, ui.card().classes('w-64 h-64'):\n        ui.label('New Content')\n    dialog.open()\n\nwith ui.dialog() as dialog, ui.card():\n    ui.label('Hello world!')\n\nui.button('Open', on_click=dialog.open)\nui.button('Replace', on_click=replace)\n\nui.run()",
    "url": "/documentation/dialog#replacing_content"
  },
  {
    "title": "ui.dialog: Events",
    "content": "Dialogs emit events when they are opened or closed.\nSee the [Quasar documentation](https://quasar.dev/vue-components/dialog) for more information.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.dialog().props('backdrop-filter=\"blur(8px) brightness(40%)\"') as dialog:\n    ui.label('Press ESC to close').classes('text-3xl text-white')\n\ndialog.on('show', lambda: ui.notify('Dialog opened'))\ndialog.on('hide', lambda: ui.notify('Dialog closed'))\ndialog.on('escape-key', lambda: ui.notify('ESC pressed'))\nui.button('Open', on_click=dialog.open)\n\nui.run()",
    "url": "/documentation/dialog#events"
  },
  {
    "title": "ui.dialog: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/dialog#reference"
  },
  {
    "title": "ui.expansion: Expansion Element",
    "content": "Provides an expandable container based on Quasar's `QExpansionItem \u003Chttps://quasar.dev/vue-components/expansion-item\u003E`_ component.\n\n:param text: title text\n:param caption: optional caption (or sub-label) text\n:param icon: optional icon (default: None)\n:param group: optional group name for coordinated open/close state within the group a.k.a. \"accordion mode\"\n:param value: whether the expansion should be opened on creation (default: `False`)\n:param on_value_change: callback to execute when value changes\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.expansion('Expand!', icon='work').classes('w-full'):\n    ui.label('inside the expansion')\n\nui.run()",
    "url": "/documentation/expansion#expansion_element"
  },
  {
    "title": "ui.expansion: Expansion with Custom Header",
    "content": "Instead of setting a plain-text title, you can fill the expansion header with UI elements by adding them to the \"header\" slot.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.expansion() as expansion:\n    with expansion.add_slot('header'):\n        ui.image('https://nicegui.io/logo.png').classes('w-16')\n    ui.label('What a nice GUI!')\n\nui.run()",
    "url": "/documentation/expansion#expansion_with_custom_header"
  },
  {
    "title": "ui.expansion: Expansion with Custom Caption",
    "content": "A caption, or sub-label, can be added below the title.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.expansion('Expand!', caption='Expansion Caption').classes('w-full'):\n    ui.label('inside the expansion')\n\nui.run()",
    "url": "/documentation/expansion#expansion_with_custom_caption"
  },
  {
    "title": "ui.expansion: Expansion with Grouping",
    "content": "An expansion group can be defined to enable coordinated open/close states a.k.a. \"accordion mode\".",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.expansion(text='Expand One!', group='group'):\n    ui.label('inside expansion one')\nwith ui.expansion(text='Expand Two!', group='group'):\n    ui.label('inside expansion two')\nwith ui.expansion(text='Expand Three!', group='group'):\n    ui.label('inside expansion three')\n\nui.run()",
    "url": "/documentation/expansion#expansion_with_grouping"
  },
  {
    "title": "ui.expansion: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/expansion#reference"
  },
  {
    "title": "ui.fullscreen: Fullscreen control element",
    "content": "This element is based on Quasar's `AppFullscreen \u003Chttps://quasar.dev/quasar-plugins/app-fullscreen\u003E`_ plugin\nand provides a way to enter, exit and toggle the fullscreen mode.\n\nImportant notes:\n\n* Due to security reasons, the fullscreen mode can only be entered from a previous user interaction such as a button click.\n* The long-press escape requirement only works in some browsers like Google Chrome or Microsoft Edge.\n\n*Added in version 2.11.0*\n\n:param require_escape_hold: whether the user needs to long-press the escape key to exit fullscreen mode\n:param on_value_change: callback which is invoked when the fullscreen state changes\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nfullscreen = ui.fullscreen()\n\nui.button('Enter Fullscreen', on_click=fullscreen.enter)\nui.button('Exit Fullscreen', on_click=fullscreen.exit)\nui.button('Toggle Fullscreen', on_click=fullscreen.toggle)\n\nui.run()",
    "url": "/documentation/fullscreen#fullscreen_control_element"
  },
  {
    "title": "ui.fullscreen: Requiring long-press to exit",
    "content": "You can require users to long-press the escape key to exit fullscreen mode.\nThis is useful to prevent accidental exits, for example when working on forms or editing data.\n\nNote that this feature only works in some browsers like Google Chrome or Microsoft Edge.",
    "format": "md",
    "demo": "from nicegui import ui\n\nfullscreen = ui.fullscreen()\nui.switch('Require escape hold').bind_value_to(fullscreen, 'require_escape_hold')\nui.button('Toggle Fullscreen', on_click=fullscreen.toggle)\n\nui.run()",
    "url": "/documentation/fullscreen#requiring_long-press_to_exit"
  },
  {
    "title": "ui.fullscreen: Tracking fullscreen state",
    "content": "You can track when the fullscreen state changes.\n\nNote that due to security reasons, fullscreen mode can only be entered from a previous user interaction\nsuch as a button click.",
    "format": "md",
    "demo": "from nicegui import ui\n\nfullscreen = ui.fullscreen(\n    on_value_change=lambda e: ui.notify('Enter' if e.value else 'Exit')\n)\nui.button('Toggle Fullscreen', on_click=fullscreen.toggle)\nui.label().bind_text_from(fullscreen, 'state',\n                          lambda state: 'Fullscreen' if state else '')\n\nui.run()",
    "url": "/documentation/fullscreen#tracking_fullscreen_state"
  },
  {
    "title": "ui.fullscreen: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/fullscreen#reference"
  },
  {
    "title": "ui.grid: Grid Element",
    "content": "Provides a container which arranges its child in a grid.\n\n:param rows: number of rows in the grid or a string with the grid-template-rows CSS property (e.g. 'auto 1fr')\n:param columns: number of columns in the grid or a string with the grid-template-columns CSS property (e.g. 'auto 1fr')\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.grid(columns=2):\n    ui.label('Name:')\n    ui.label('Tom')\n\n    ui.label('Age:')\n    ui.label('42')\n\n    ui.label('Height:')\n    ui.label('1.80m')\n\nui.run()",
    "url": "/documentation/grid#grid_element"
  },
  {
    "title": "ui.grid: Custom grid layout",
    "content": "This demo shows how to create a custom grid layout passing a string with the grid-template-columns CSS property.\nYou can use any valid CSS dimensions, such as 'auto', '1fr', '80px', etc.\n\n- 'auto' will make the column as wide as its content.\n- '1fr' or '2fr' will make the corresponding columns fill the remaining space, with fractions in a 1:2 ratio.\n- '80px' will make the column 80 pixels wide.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.grid(columns='auto 80px 1fr 2fr').classes('w-full gap-0'):\n    for _ in range(3):\n        ui.label('auto').classes('border p-1')\n        ui.label('80px').classes('border p-1')\n        ui.label('1fr').classes('border p-1')\n        ui.label('2fr').classes('border p-1')\n\nui.run()",
    "url": "/documentation/grid#custom_grid_layout"
  },
  {
    "title": "ui.grid: Cells spanning multiple columns",
    "content": "This demo shows how to span cells over multiple columns.\n\nNote that there is [no Tailwind class for spanning 15 columns](https://v3.tailwindcss.com/docs/grid-column#arbitrary-values),\nbut we can set [arbitrary values](https://v3.tailwindcss.com/docs/grid-column#arbitrary-values) using square brackets.\nAlternatively you could use the corresponding CSS definition: `.style('grid-column: span 15 / span 15')`.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.grid(columns=16).classes('w-full gap-0'):\n    ui.label('full').classes('col-span-full border p-1')\n    ui.label('8').classes('col-span-8 border p-1')\n    ui.label('8').classes('col-span-8 border p-1')\n    ui.label('12').classes('col-span-12 border p-1')\n    ui.label('4').classes('col-span-4 border p-1')\n    ui.label('15').classes('col-[span_15] border p-1')\n    ui.label('1').classes('col-span-1 border p-1')\n\nui.run()",
    "url": "/documentation/grid#cells_spanning_multiple_columns"
  },
  {
    "title": "ui.grid: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/grid#reference"
  },
  {
    "title": "ui.list: List",
    "content": "A list element based on Quasar's `QList \u003Chttps://quasar.dev/vue-components/list-and-list-items#qlist-api\u003E`_ component.\nIt provides a container for ``ui.item`` elements.\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.list().props('dense separator'):\n    ui.item('3 Apples')\n    ui.item('5 Bananas')\n    ui.item('8 Strawberries')\n    ui.item('13 Walnuts')\n\nui.run()",
    "url": "/documentation/list#list"
  },
  {
    "title": "ui.list: Items, Sections and Labels",
    "content": "List items use item sections to structure their content.\nItem labels take different positions depending on their props.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.list().props('bordered separator'):\n    ui.item_label('Contacts').props('header').classes('text-bold')\n    ui.separator()\n    with ui.item(on_click=lambda: ui.notify('Selected contact 1')):\n        with ui.item_section().props('avatar'):\n            ui.icon('person')\n        with ui.item_section():\n            ui.item_label('Nice Guy')\n            ui.item_label('name').props('caption')\n        with ui.item_section().props('side'):\n            ui.icon('chat')\n    with ui.item(on_click=lambda: ui.notify('Selected contact 2')):\n        with ui.item_section().props('avatar'):\n            ui.icon('person')\n        with ui.item_section():\n            ui.item_label('Nice Person')\n            ui.item_label('name').props('caption')\n        with ui.item_section().props('side'):\n            ui.icon('chat')\n\nui.run()",
    "url": "/documentation/list#items__sections_and_labels"
  },
  {
    "title": "ui.list: Reference for ui.list",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/list#reference_for_ui_list"
  },
  {
    "title": "ui.list: Reference for ui.item",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/list#reference_for_ui_item"
  },
  {
    "title": "ui.list: Reference for ui.item_section",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/list#reference_for_ui_item_section"
  },
  {
    "title": "ui.list: Reference for ui.item_label",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/list#reference_for_ui_item_label"
  },
  {
    "title": "ui.menu: Menu",
    "content": "Creates a menu based on Quasar's `QMenu \u003Chttps://quasar.dev/vue-components/menu\u003E`_ component.\nThe menu should be placed inside the element where it should be shown.\n\nAdvanced tip:\nUse the `auto-close` prop to automatically close the menu on any click event directly without a server round-trip.\n\n:param value: whether the menu is already opened (default: `False`)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.row().classes('w-full items-center'):\n    result = ui.label().classes('mr-auto')\n    with ui.button(icon='menu'):\n        with ui.menu() as menu:\n            ui.menu_item('Menu item 1', lambda: result.set_text('Selected item 1'))\n            ui.menu_item('Menu item 2', lambda: result.set_text('Selected item 2'))\n            ui.menu_item('Menu item 3 (keep open)',\n                         lambda: result.set_text('Selected item 3'), auto_close=False)\n            ui.separator()\n            ui.menu_item('Close', menu.close)\n\nui.run()",
    "url": "/documentation/menu#menu"
  },
  {
    "title": "ui.menu: Client-side auto-close",
    "content": "Use the `auto-close` prop to automatically close the menu on any click event directly without a server round-trip.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.button(icon='menu'):\n    with ui.menu().props('auto-close'):\n        toggle = ui.toggle(['fastfood', 'cake', 'icecream'], value='fastfood')\nui.icon('', size='md').bind_name_from(toggle, 'value')\n\nui.run()",
    "url": "/documentation/menu#client-side_auto-close"
  },
  {
    "title": "ui.menu: Menu with sub-menus",
    "content": "You can use a `ui.menu` nested inside a `ui.menu_item` to created nested sub-menus.\nThe \"anchor\" and \"self\" props can be used to position the sub-menu.\nMake sure to disable `auto-close` on the corresponding menu item to keep the menu open while navigating the sub-menu.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.button(icon='menu'):\n    with ui.menu():\n        ui.menu_item('Option 1')\n        ui.menu_item('Option 2')\n        with ui.menu_item('Option 3', auto_close=False):\n            with ui.item_section().props('side'):\n                ui.icon('keyboard_arrow_right')\n            with ui.menu().props('anchor=\"top end\" self=\"top start\" auto-close'):\n                ui.menu_item('Sub-option 1')\n                ui.menu_item('Sub-option 2')\n                ui.menu_item('Sub-option 3')\n\nui.run()",
    "url": "/documentation/menu#menu_with_sub-menus"
  },
  {
    "title": "ui.menu: Reference for ui.menu",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/menu#reference_for_ui_menu"
  },
  {
    "title": "ui.menu: Reference for ui.menu_item",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/menu#reference_for_ui_menu_item"
  },
  {
    "title": "ui.slide_item: Slide Item",
    "content": "This element is based on Quasar's `QSlideItem \u003Chttps://quasar.dev/vue-components/slide-item/\u003E`_ component.\n\nIf the ``text`` parameter is provided, a nested ``ui.item`` element will be created with the given text.\nIf you want to customize how the text is displayed, you can place custom elements inside the slide item.\n\nTo fill slots for individual slide actions, use the ``left``, ``right``, ``top``, or ``bottom`` methods or\nthe ``action`` method with a side argument (\"left\", \"right\", \"top\", or \"bottom\").\n\nOnce a slide action has occurred, the slide item can be reset back to its initial state using the ``reset`` method.\n\n*Added in version 2.12.0*\n\n:param text: text to be displayed (default: \"\")\n:param on_slide: callback which is invoked when any slide action is activated\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.list().props('bordered separator'):\n    with ui.slide_item('Slide me left or right') as slide_item_1:\n        slide_item_1.left('Left', color='green')\n        slide_item_1.right('Right', color='red')\n    with ui.slide_item('Slide me up or down') as slide_item_2:\n        slide_item_2.top('Top', color='blue')\n        slide_item_2.bottom('Bottom', color='purple')\n\nui.run()",
    "url": "/documentation/slide_item#slide_item"
  },
  {
    "title": "ui.slide_item: More complex layout",
    "content": "You can fill the slide item and its action slots with custom UI elements.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.list().props('bordered'):\n    with ui.slide_item() as slide_item:\n        with ui.item():\n            with ui.item_section().props('avatar'):\n                ui.icon('person')\n            with ui.item_section():\n                ui.item_label('Alice A. Anderson')\n                ui.item_label('CEO').props('caption')\n        with slide_item.left(on_slide=lambda: ui.notify('Calling...')):\n            with ui.item(on_click=slide_item.reset):\n                with ui.item_section().props('avatar'):\n                    ui.icon('phone')\n                ui.item_section('Call')\n        with slide_item.right(on_slide=lambda: ui.notify('Texting...')):\n            with ui.item(on_click=slide_item.reset):\n                ui.item_section('Text')\n                with ui.item_section().props('avatar'):\n                    ui.icon('message')\n\nui.run()",
    "url": "/documentation/slide_item#more_complex_layout"
  },
  {
    "title": "ui.slide_item: Slide handlers",
    "content": "An event handler can be triggered when a specific side is selected.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.list().props('bordered'):\n    with ui.slide_item('Slide me', on_slide=lambda e: ui.notify(f'Slide: {e.side}')) as slide_item:\n        slide_item.left('A', on_slide=lambda e: ui.notify(f'A ({e.side})'))\n        slide_item.right('B', on_slide=lambda e: ui.notify(f'B ({e.side})'))\n\nui.run()",
    "url": "/documentation/slide_item#slide_handlers"
  },
  {
    "title": "ui.slide_item: Resetting the slide item",
    "content": "After a slide action has occurred, the slide item can be reset back to its initial state using the ``reset`` method.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.list().props('bordered'):\n    with ui.slide_item() as slide_item:\n        ui.item('Slide me')\n        with slide_item.left(color='blue'):\n            ui.item('Left')\n        with slide_item.right(color='purple'):\n            ui.item('Right')\n\nui.button('Reset', on_click=slide_item.reset)\n\nui.run()",
    "url": "/documentation/slide_item#resetting_the_slide_item"
  },
  {
    "title": "ui.slide_item: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/slide_item#reference"
  },
  {
    "title": "ui.notification: Notification element",
    "content": "Displays a notification on the screen.\nIn contrast to `ui.notify`, this element allows to update the notification message and other properties once the notification is displayed.\nThe notification can be removed with `dismiss()`.\n\n:param message: content of the notification\n:param position: position on the screen (\"top-left\", \"top-right\", \"bottom-left\", \"bottom-right\", \"top\", \"bottom\", \"left\", \"right\" or \"center\", default: \"bottom\")\n:param close_button: optional label of a button to dismiss the notification (default: `False`)\n:param type: optional type (\"positive\", \"negative\", \"warning\", \"info\" or \"ongoing\")\n:param color: optional color name\n:param multi_line: enable multi-line notifications\n:param icon: optional name of an icon to be displayed in the notification (default: `None`)\n:param spinner: display a spinner in the notification (default: False)\n:param timeout: optional timeout in seconds after which the notification is dismissed (default: 5.0)\n:param on_dismiss: optional callback to be invoked when the notification is dismissed\n:param options: optional dictionary with all options (overrides all other arguments)\n\nNote: You can pass additional keyword arguments according to `Quasar's Notify API \u003Chttps://quasar.dev/quasar-plugins/notify#notify-api\u003E`_.\n",
    "format": "rst",
    "demo": "import asyncio\nfrom nicegui import ui\n\nasync def compute():\n    n = ui.notification(timeout=None)\n    for i in range(10):\n        n.message = f'Computing {i/10:.0%}'\n        n.spinner = True\n        await asyncio.sleep(0.2)\n    n.message = 'Done!'\n    n.spinner = False\n    await asyncio.sleep(1)\n    n.dismiss()\n\nui.button('Compute', on_click=compute)\n\nui.run()",
    "url": "/documentation/notification#notification_element"
  },
  {
    "title": "ui.notification: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/notification#reference"
  },
  {
    "title": "ui.notify: Notification",
    "content": "Displays a notification on the screen.\n\n:param message: content of the notification\n:param position: position on the screen (\"top-left\", \"top-right\", \"bottom-left\", \"bottom-right\", \"top\", \"bottom\", \"left\", \"right\" or \"center\", default: \"bottom\")\n:param close_button: optional label of a button to dismiss the notification (default: `False`)\n:param type: optional type (\"positive\", \"negative\", \"warning\", \"info\" or \"ongoing\")\n:param color: optional color name\n:param multi_line: enable multi-line notifications\n\nNote: You can pass additional keyword arguments according to `Quasar's Notify API \u003Chttps://quasar.dev/quasar-plugins/notify#notify-api\u003E`_.\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.button('Say hi!', on_click=lambda: ui.notify('Hi!', close_button='OK'))\n\nui.run()",
    "url": "/documentation/notify#notification"
  },
  {
    "title": "ui.notify: Notification Types",
    "content": "There are different types that can be used to indicate the nature of the notification.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.button('negative', on_click=lambda: ui.notify('error', type='negative'))\nui.button('positive', on_click=lambda: ui.notify('success', type='positive'))\nui.button('warning', on_click=lambda: ui.notify('warning', type='warning'))\n\nui.run()",
    "url": "/documentation/notify#notification_types"
  },
  {
    "title": "ui.notify: Multiline Notifications",
    "content": "To allow a notification text to span multiple lines, it is sufficient to set `multi_line=True`.\nIf manual newline breaks are required (e.g. `\\n`), you need to define a CSS style and pass it to the notification as shown in the example.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.html('\u003Cstyle\u003E.multi-line-notification { white-space: pre-line; }\u003C/style\u003E')\nui.button('show', on_click=lambda: ui.notify(\n    'Lorem ipsum dolor sit amet, consectetur adipisicing elit. \\n'\n    'Hic quisquam non ad sit assumenda consequuntur esse inventore officia. \\n'\n    'Corrupti reiciendis impedit vel, '\n    'fugit odit quisquam quae porro exercitationem eveniet quasi.',\n    multi_line=True,\n    classes='multi-line-notification',\n))\n\nui.run()",
    "url": "/documentation/notify#multiline_notifications"
  },
  {
    "title": "ui.pagination: Pagination",
    "content": "A pagination element wrapping Quasar's `QPagination \u003Chttps://quasar.dev/vue-components/pagination\u003E`_ component.\n\n:param min: minimum page number\n:param max: maximum page number\n:param direction_links: whether to show first/last page links\n:param value: initial page (defaults to `min` if no value is provided)\n:param on_change: callback to be invoked when the value changes\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\np = ui.pagination(1, 5, direction_links=True)\nui.label().bind_text_from(p, 'value', lambda v: f'Page {v}')\n\nui.run()",
    "url": "/documentation/pagination#pagination"
  },
  {
    "title": "ui.pagination: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/pagination#reference"
  },
  {
    "title": "ui.row: Row Element",
    "content": "Provides a container which arranges its child in a row.\n\n:param wrap: whether to wrap the content (default: `True`)\n:param align_items: alignment of the items in the row (\"start\", \"end\", \"center\", \"baseline\", or \"stretch\"; default: `None`)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.row():\n    ui.label('label 1')\n    ui.label('label 2')\n    ui.label('label 3')\n\nui.run()",
    "url": "/documentation/row#row_element"
  },
  {
    "title": "ui.row: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/row#reference"
  },
  {
    "title": "ui.scroll_area: Scroll Area",
    "content": "A way of customizing the scrollbars by encapsulating your content.\nThis element exposes the Quasar `ScrollArea \u003Chttps://quasar.dev/vue-components/scroll-area/\u003E`_ component.\n\n:param on_scroll: function to be called when the scroll position changes\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.row():\n    with ui.scroll_area().classes('w-32 h-32 border'):\n        ui.label('I scroll. ' * 20)\n    with ui.column().classes('p-4 w-32 h-32 border'):\n        ui.label('I will not scroll. ' * 10)\n\nui.run()",
    "url": "/documentation/scroll_area#scroll_area"
  },
  {
    "title": "ui.scroll_area: Handling Scroll Events",
    "content": "You can use the `on_scroll` argument in `ui.scroll_area` to handle scroll events.\nThe callback receives a `ScrollEventArguments` object with the following attributes:\n\n- `sender`: the scroll area that generated the event\n- `client`: the matching client\n- additional arguments as described in [Quasar's documentation for the ScrollArea API](https://quasar.dev/vue-components/scroll-area/#qscrollarea-api)",
    "format": "md",
    "demo": "from nicegui import ui\n\nposition = ui.number('scroll position:').props('readonly')\nwith ui.card().classes('w-32 h-32'):\n    with ui.scroll_area(on_scroll=lambda e: position.set_value(e.vertical_percentage)):\n        ui.label('I scroll. ' * 20)\n\nui.run()",
    "url": "/documentation/scroll_area#handling_scroll_events"
  },
  {
    "title": "ui.scroll_area: Setting the scroll position",
    "content": "You can use `scroll_to` to programmatically set the scroll position.\nThis can be useful for navigation or synchronization of multiple scroll areas.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.number('position', value=0, min=0, max=1, step=0.1,\n          on_change=lambda e: area1.scroll_to(percent=e.value)).classes('w-32')\n\nwith ui.row():\n    with ui.card().classes('w-32 h-48'):\n        with ui.scroll_area(on_scroll=lambda e: area2.scroll_to(percent=e.vertical_percentage)) as area1:\n            ui.label('I scroll. ' * 20)\n\n    with ui.card().classes('w-32 h-48'):\n        with ui.scroll_area() as area2:\n            ui.label('I scroll. ' * 20)\n\nui.run()",
    "url": "/documentation/scroll_area#setting_the_scroll_position"
  },
  {
    "title": "ui.scroll_area: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/scroll_area#reference"
  },
  {
    "title": "ui.separator: Separator",
    "content": "This element is based on Quasar's `QSeparator \u003Chttps://quasar.dev/vue-components/separator\u003E`_ component.\n\nIt serves as a separator for cards, menus and other component containers and is similar to HTML's \u003Chr\u003E tag.\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.label('text above')\nui.separator()\nui.label('text below')\n\nui.run()",
    "url": "/documentation/separator#separator"
  },
  {
    "title": "ui.separator: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/separator#reference"
  },
  {
    "title": "ui.skeleton: Skeleton",
    "content": "This element is based on Quasar's `QSkeleton \u003Chttps://quasar.dev/vue-components/skeleton\u003E`_ component.\nIt serves as a placeholder for loading content in cards, menus and other component containers.\nSee the `Quasar documentation \u003Chttps://quasar.dev/vue-components/skeleton/#predefined-types\u003E`_ for a list of available types.\n\n:param type: type of skeleton to display (default: \"rect\")\n:param tag: HTML tag to use for this element (default: \"div\")\n:param animation: animation effect of the skeleton placeholder (default: \"wave\")\n:param animation_speed: animation speed in seconds (default: 1.5)\n:param square: whether to remover border-radius so borders are squared (default: ``False``)\n:param bordered: whether to apply a default border to the component (default: ``False``)\n:param size: size in CSS units (overrides ``width`` and ``height``)\n:param width: width in CSS units (overridden by ``size`` if set)\n:param height: height in CSS units (overridden by ``size`` if set)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.skeleton().classes('w-full')\n\nui.run()",
    "url": "/documentation/skeleton#skeleton"
  },
  {
    "title": "ui.skeleton: Styling and animation",
    "content": "The `square` and `bordered` parameters can be set to `True` to remove the border-radius and add a border to the skeleton.\n\nThe `animation` parameter can be set to \"pulse\", \"wave\", \"pulse-x\", \"pulse-y\", \"fade\", \"blink\", or \"none\"\nto change the animation effect.\nThe default value is \"wave\".",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.skeleton('QToolbar', square=True, bordered=True, animation='pulse-y') \\\n    .classes('w-full')\n\nui.run()",
    "url": "/documentation/skeleton#styling_and_animation"
  },
  {
    "title": "ui.skeleton: YouTube Skeleton",
    "content": "Here is an example skeleton for a YouTube video.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.card().tight().classes('w-full'):\n    ui.skeleton(square=True, animation='fade', height='150px', width='100%')\n    with ui.card_section().classes('w-full'):\n        ui.skeleton('text').classes('text-subtitle1')\n        ui.skeleton('text').classes('text-subtitle1 w-1/2')\n        ui.skeleton('text').classes('text-caption')\n\nui.run()",
    "url": "/documentation/skeleton#youtube_skeleton"
  },
  {
    "title": "ui.space: Space",
    "content": "This element is based on Quasar's `QSpace \u003Chttps://quasar.dev/vue-components/space\u003E`_ component.\n\nIts purpose is to simply fill all available space inside of a flexbox element.\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.row().classes('w-full border'):\n    ui.label('Left')\n    ui.space()\n    ui.label('Right')\n\nui.run()",
    "url": "/documentation/space#space"
  },
  {
    "title": "ui.space: Vertical space",
    "content": "This element can also be used to fill vertical space.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.column().classes('h-32 border'):\n    ui.label('Top')\n    ui.space()\n    ui.label('Bottom')\n\nui.run()",
    "url": "/documentation/space#vertical_space"
  },
  {
    "title": "ui.space: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/space#reference"
  },
  {
    "title": "ui.splitter: Splitter",
    "content": "The `ui.splitter` element divides the screen space into resizable sections,\nallowing for flexible and responsive layouts in your application.\n\nBased on Quasar's Splitter component:\n`Splitter \u003Chttps://quasar.dev/vue-components/splitter\u003E`_\n\nIt provides three customizable slots, ``before``, ``after``, and ``separator``,\nwhich can be used to embed other elements within the splitter.\n\n:param horizontal: Whether to split horizontally instead of vertically\n:param limits: Two numbers representing the minimum and maximum split size of the two panels\n:param value: Size of the first panel (or second if using reverse)\n:param reverse: Whether to apply the model size to the second panel instead of the first\n:param on_change: callback which is invoked when the user releases the splitter\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.splitter() as splitter:\n    with splitter.before:\n        ui.label('This is some content on the left hand side.').classes('mr-2')\n    with splitter.after:\n        ui.label('This is some content on the right hand side.').classes('ml-2')\n\nui.run()",
    "url": "/documentation/splitter#splitter"
  },
  {
    "title": "ui.splitter: Advanced usage",
    "content": "This demo shows all the slots and parameters including a tooltip, a custom separator, and a callback.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.splitter(horizontal=False, reverse=False, value=60,\n                 on_change=lambda e: ui.notify(e.value)) as splitter:\n    ui.tooltip('This is the default slot.').classes('bg-green')\n    with splitter.before:\n        ui.label('This is the left hand side.').classes('mr-2')\n    with splitter.after:\n        ui.label('This is the right hand side.').classes('ml-2')\n    with splitter.separator:\n        ui.icon('lightbulb').classes('text-green')\n\nui.number('Split value', format='%.1f').bind_value(splitter)\n\nui.run()",
    "url": "/documentation/splitter#advanced_usage"
  },
  {
    "title": "ui.splitter: Image fun",
    "content": "This demo shows how to use the splitter to display images side by side.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.splitter().classes('w-72 h-48') \\\n        .props('before-class=overflow-hidden after-class=overflow-hidden') as splitter:\n    with splitter.before:\n        ui.image('https://cdn.quasar.dev/img/parallax1.jpg').classes('w-72 absolute-top-left')\n    with splitter.after:\n        ui.image('https://cdn.quasar.dev/img/parallax1-bw.jpg').classes('w-72 absolute-top-right')\n\nui.run()",
    "url": "/documentation/splitter#image_fun"
  },
  {
    "title": "ui.splitter: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/splitter#reference"
  },
  {
    "title": "ui.stepper: Stepper",
    "content": "This element represents `Quasar's QStepper \u003Chttps://quasar.dev/vue-components/stepper#qstepper-api\u003E`_ component.\nIt contains individual steps.\n\nTo avoid issues with dynamic elements when switching steps,\nthis element uses Vue's `keep-alive \u003Chttps://vuejs.org/guide/built-ins/keep-alive.html\u003E`_ component.\nIf client-side performance is an issue, you can disable this feature.\n\n:param value: `ui.step` or name of the step to be initially selected (default: `None` meaning the first step)\n:param on_value_change: callback to be executed when the selected step changes\n:param keep_alive: whether to use Vue's keep-alive component on the content (default: `True`)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.stepper().props('vertical').classes('w-full') as stepper:\n    with ui.step('Preheat'):\n        ui.label('Preheat the oven to 350 degrees')\n        with ui.stepper_navigation():\n            ui.button('Next', on_click=stepper.next)\n    with ui.step('Ingredients'):\n        ui.label('Mix the ingredients')\n        with ui.stepper_navigation():\n            ui.button('Next', on_click=stepper.next)\n            ui.button('Back', on_click=stepper.previous).props('flat')\n    with ui.step('Bake'):\n        ui.label('Bake for 20 minutes')\n        with ui.stepper_navigation():\n            ui.button('Done', on_click=lambda: ui.notify('Yay!', type='positive'))\n            ui.button('Back', on_click=stepper.previous).props('flat')\n\nui.run()",
    "url": "/documentation/stepper#stepper"
  },
  {
    "title": "ui.stepper: Dynamic Stepper",
    "content": "Steps can be added dynamically and positioned via `ui.move()`.",
    "format": "md",
    "demo": "from nicegui import ui\n\ndef next_step() -\u003E None:\n    if extra_step.value and len(stepper.default_slot.children) == 2:\n        with stepper:\n            with ui.step('extra') as extra:\n                ui.label('Extra')\n                with ui.stepper_navigation():\n                    ui.button('Back', on_click=stepper.previous).props('flat')\n                    ui.button('Next', on_click=stepper.next)\n            extra.move(target_index=1)\n    stepper.next()\n\nwith ui.stepper().props('vertical').classes('w-full') as stepper:\n    with ui.step('start'):\n        ui.label('Start')\n        extra_step = ui.checkbox('do extra step')\n        with ui.stepper_navigation():\n            ui.button('Next', on_click=next_step)\n    with ui.step('finish'):\n        ui.label('Finish')\n        with ui.stepper_navigation():\n            ui.button('Back', on_click=stepper.previous).props('flat')\n\nui.run()",
    "url": "/documentation/stepper#dynamic_stepper"
  },
  {
    "title": "ui.stepper: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/stepper#reference"
  },
  {
    "title": "Tabs: Tabs",
    "content": "The elements `ui.tabs`, `ui.tab`, `ui.tab_panels`, and `ui.tab_panel` resemble\n[Quasar's tabs](https://quasar.dev/vue-components/tabs) and\n[tab panels](https://quasar.dev/vue-components/tab-panels) API.\n\n`ui.tabs` creates a container for the tabs. This could be placed in a `ui.header` for example.\n`ui.tab_panels` creates a container for the tab panels with the actual content.\nEach `ui.tab_panel` is associated with a `ui.tab` element.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.tabs().classes('w-full') as tabs:\n    one = ui.tab('One')\n    two = ui.tab('Two')\nwith ui.tab_panels(tabs, value=two).classes('w-full'):\n    with ui.tab_panel(one):\n        ui.label('First tab')\n    with ui.tab_panel(two):\n        ui.label('Second tab')\n\nui.run()",
    "url": "/documentation/tabs#tabs"
  },
  {
    "title": "Tabs: Name, label, icon",
    "content": "The `ui.tab` element has a `label` property that can be used to display a different text than the `name`.\nThe `name` can also be used instead of the `ui.tab` objects to associate a `ui.tab` with a `ui.tab_panel`.\nAdditionally each tab can have an `icon`.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.tabs() as tabs:\n    ui.tab('h', label='Home', icon='home')\n    ui.tab('a', label='About', icon='info')\nwith ui.tab_panels(tabs, value='h').classes('w-full'):\n    with ui.tab_panel('h'):\n        ui.label('Main Content')\n    with ui.tab_panel('a'):\n        ui.label('Infos')\n\nui.run()",
    "url": "/documentation/tabs#name__label__icon"
  },
  {
    "title": "Tabs: Switch tabs programmatically",
    "content": "The `ui.tabs` and `ui.tab_panels` elements are derived from ValueElement which has a `set_value` method.\nThat can be used to switch tabs programmatically.",
    "format": "md",
    "demo": "from nicegui import ui\n\ncontent = {'Tab 1': 'Content 1', 'Tab 2': 'Content 2', 'Tab 3': 'Content 3'}\nwith ui.tabs() as tabs:\n    for title in content:\n        ui.tab(title)\nwith ui.tab_panels(tabs).classes('w-full') as panels:\n    for title, text in content.items():\n        with ui.tab_panel(title):\n            ui.label(text)\n\nui.button('GoTo 1', on_click=lambda: panels.set_value('Tab 1'))\nui.button('GoTo 2', on_click=lambda: tabs.set_value('Tab 2'))\n\nui.run()",
    "url": "/documentation/tabs#switch_tabs_programmatically"
  },
  {
    "title": "Tabs: Vertical tabs with splitter",
    "content": "Like in [Quasar's vertical tabs example](https://quasar.dev/vue-components/tabs#vertical),\nwe can combine `ui.splitter` and tab elements to create a vertical tabs layout.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.splitter(value=30).classes('w-full h-56') as splitter:\n    with splitter.before:\n        with ui.tabs().props('vertical').classes('w-full') as tabs:\n            mail = ui.tab('Mails', icon='mail')\n            alarm = ui.tab('Alarms', icon='alarm')\n            movie = ui.tab('Movies', icon='movie')\n    with splitter.after:\n        with ui.tab_panels(tabs, value=mail) \\\n                .props('vertical').classes('w-full h-full'):\n            with ui.tab_panel(mail):\n                ui.label('Mails').classes('text-h4')\n                ui.label('Content of mails')\n            with ui.tab_panel(alarm):\n                ui.label('Alarms').classes('text-h4')\n                ui.label('Content of alarms')\n            with ui.tab_panel(movie):\n                ui.label('Movies').classes('text-h4')\n                ui.label('Content of movies')\n\nui.run()",
    "url": "/documentation/tabs#vertical_tabs_with_splitter"
  },
  {
    "title": "Tabs: Reference for ui.tabs",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/tabs#reference_for_ui_tabs"
  },
  {
    "title": "Tabs: Reference for ui.tab",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/tabs#reference_for_ui_tab"
  },
  {
    "title": "Tabs: Reference for ui.tab_panels",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/tabs#reference_for_ui_tab_panels"
  },
  {
    "title": "Tabs: Reference for ui.tab_panel",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/tabs#reference_for_ui_tab_panel"
  },
  {
    "title": "ui.teleport: Teleport",
    "content": "An element that allows us to transmit the content from within a component to any location on the page.\n\n:param to: NiceGUI element or CSS selector of the target element for the teleported content\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nmarkdown = ui.markdown('Enter your **name**!')\n\ndef inject_input():\n    with ui.teleport(f'#{markdown.html_id} strong'):\n        ui.input('name').classes('inline-flex').props('dense outlined')\n\nui.button('inject input', on_click=inject_input)\n\nui.run()",
    "url": "/documentation/teleport#teleport"
  },
  {
    "title": "ui.teleport: Radio element with arbitrary content",
    "content": "With the right CSS selector, you can place any content inside a standard radio element.",
    "format": "md",
    "demo": "from nicegui import ui\n\noptions = ['Star', 'Thump Up', 'Heart']\nradio = ui.radio({x: '' for x in options}, value='Star').props('inline')\nwith ui.teleport(f'#{radio.html_id} \u003E div:nth-child(1) .q-radio__label'):\n    ui.icon('star', size='md')\nwith ui.teleport(f'#{radio.html_id} \u003E div:nth-child(2) .q-radio__label'):\n    ui.icon('thumb_up', size='md')\nwith ui.teleport(f'#{radio.html_id} \u003E div:nth-child(3) .q-radio__label'):\n    ui.icon('favorite', size='md')\nui.label().bind_text_from(radio, 'value')\n\nui.run()",
    "url": "/documentation/teleport#radio_element_with_arbitrary_content"
  },
  {
    "title": "ui.teleport: Injecting a graph into a table cell",
    "content": "This demo shows how to inject ECharts graphs into table cells.",
    "format": "md",
    "demo": "from nicegui import ui\n\ncolumns = [\n    {'name': 'name', 'label': 'Product', 'field': 'name', 'align': 'center'},\n    {'name': 'sales', 'label': 'Sales', 'field': 'sales', 'align': 'center'},\n]\nrows = [\n    {'name': 'A', 'data': [10, 8, 2, 4]},\n    {'name': 'B', 'data': [3, 5, 7, 8]},\n    {'name': 'C', 'data': [2, 1, 3, 7]},\n]\ntable = ui.table(columns=columns, rows=rows, row_key='name').classes('w-72')\nfor r, row in enumerate(rows):\n    with ui.teleport(f'#{table.html_id} tr:nth-child({r+1}) td:nth-child(2)'):\n        ui.echart({\n            'xAxis': {'type': 'category', 'show': False},\n            'yAxis': {'type': 'value', 'show': False},\n            'series': [{'type': 'line', 'data': row['data']}],\n        }).classes('w-44 h-20')\n\nui.run()",
    "url": "/documentation/teleport#injecting_a_graph_into_a_table_cell"
  },
  {
    "title": "ui.teleport: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/teleport#reference"
  },
  {
    "title": "ui.timeline: Timeline",
    "content": "This element represents `Quasar's QTimeline \u003Chttps://quasar.dev/vue-components/timeline#qtimeline-api\u003E`_ component.\n\n:param side: Side (\"left\" or \"right\"; default: \"left\").\n:param layout: Layout (\"dense\", \"comfortable\" or \"loose\"; default: \"dense\").\n:param color: Color of the icons.\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.timeline(side='right'):\n    ui.timeline_entry('Rodja and Falko start working on NiceGUI.',\n                      title='Initial commit',\n                      subtitle='May 07, 2021')\n    ui.timeline_entry('The first PyPI package is released.',\n                      title='Release of 0.1',\n                      subtitle='May 14, 2021')\n    ui.timeline_entry('Large parts are rewritten to remove JustPy '\n                      'and to upgrade to Vue 3 and Quasar 2.',\n                      title='Release of 1.0',\n                      subtitle='December 15, 2022',\n                      icon='rocket')\n\nui.run()",
    "url": "/documentation/timeline#timeline"
  },
  {
    "title": "ui.timeline: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/timeline#reference"
  },
  {
    "title": "ui.tooltip: Tooltip",
    "content": "This element is based on Quasar's `QTooltip \u003Chttps://quasar.dev/vue-components/tooltip\u003E`_ component.\nIt can be placed in another element to show additional information on hover.\n\nInstead of passing a string as the first argument, you can also nest other elements inside the tooltip.\n\n:param text: the content of the tooltip (default: '')\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.button(icon='thumb_up'):\n    ui.tooltip('I like this').classes('bg-green')\n\nui.run()",
    "url": "/documentation/tooltip#tooltip"
  },
  {
    "title": "ui.tooltip: Tooltip method",
    "content": "Instead of nesting a tooltip element inside another element, you can also use the `tooltip` method.\n\nNote that with this method you cannot apply additional properties (props) or styling directly to the tooltip.\nIf you need custom styling or properties, nest a `ui.tooltip` element instead.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.label('Tooltips...').tooltip('...are shown on mouse over')\n\nui.run()",
    "url": "/documentation/tooltip#tooltip_method"
  },
  {
    "title": "ui.tooltip: Tooltip with HTML",
    "content": "You can use HTML in tooltips by nesting a `ui.html` element.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.label('HTML...'):\n    with ui.tooltip():\n        ui.html('\u003Cb\u003Eb\u003C/b\u003E, \u003Cem\u003Eem\u003C/em\u003E, \u003Cu\u003Eu\u003C/u\u003E, \u003Cs\u003Es\u003C/s\u003E')\n\nui.run()",
    "url": "/documentation/tooltip#tooltip_with_html"
  },
  {
    "title": "ui.tooltip: Tooltip with other content",
    "content": "Other elements like `ui.images` can also be nested inside a tooltip.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.label('Mountains...'):\n    with ui.tooltip().classes('bg-transparent'):\n        ui.image('https://picsum.photos/id/377/640/360').classes('w-64')\n\nui.run()",
    "url": "/documentation/tooltip#tooltip_with_other_content"
  },
  {
    "title": "ui.tooltip: Tooltip on HTML and Markdown",
    "content": "Some elements like `ui.html` and `ui.markdown` do not support nested elements.\nIn this case, you can nest such elements inside a container element with a tooltip.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.element().tooltip('...with a tooltip!'):\n    ui.html('This is \u003Cu\u003EHTML\u003C/u\u003E...')\n\nui.run()",
    "url": "/documentation/tooltip#tooltip_on_html_and_markdown"
  },
  {
    "title": "ui.tooltip: Tooltip for the upload element",
    "content": "Components like `ui.upload` do not support tooltips directly.\nYou can wrap them in a `ui.element` to add tooltips and props.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.element():\n    ui.upload(on_upload=lambda e: ui.notify(f'Uploaded {e.name}')).classes('w-72')\n    ui.tooltip('Upload files').props('delay=1000 transition-show=rotate')\n\nui.run()",
    "url": "/documentation/tooltip#tooltip_for_the_upload_element"
  },
  {
    "title": "ui.tooltip: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/tooltip#reference"
  },
  {
    "title": "Page Layout: Auto-context",
    "content": "In order to allow writing intuitive UI descriptions, NiceGUI automatically tracks the context in which elements are created.\nThis means that there is no explicit `parent` parameter.\nInstead the parent context is defined using a `with` statement.\nIt is also passed to event handlers and timers.\n\nIn the demo, the label \"Card content\" is added to the card.\nAnd because the `ui.button` is also added to the card, the label \"Click!\" will also be created in this context.\nThe label \"Tick!\", which is added once after one second, is also added to the card.\n\nThis design decision allows for easily creating modular components that keep working after moving them around in the UI.\nFor example, you can move label and button somewhere else, maybe wrap them in another container, and the code will still work.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.card():\n    ui.label('Card content')\n    ui.button('Add label', on_click=lambda: ui.label('Click!'))\n    ui.timer(1.0, lambda: ui.label('Tick!'), once=True)\n\nui.run()",
    "url": "/documentation/section_page_layout#auto-context"
  },
  {
    "title": "Page Layout: Card",
    "content": "This element is based on Quasar's `QCard \u003Chttps://quasar.dev/vue-components/card\u003E`_ component.\nIt provides a container with a dropped shadow.\n\nNote:\nIn contrast to this element,\nthe original QCard has no padding by default and hides outer borders and shadows of nested elements.\nIf you want the original behavior, use the `tight` method.\n\n*Updated in version 2.0.0: Don't hide outer borders and shadows of nested elements anymore.*\n\n:param align_items: alignment of the items in the card (\"start\", \"end\", \"center\", \"baseline\", or \"stretch\"; default: `None`)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.card().tight():\n    ui.image('https://picsum.photos/id/684/640/360')\n    with ui.card_section():\n        ui.label('Lorem ipsum dolor sit amet, consectetur adipiscing elit, ...')\n\nui.run()",
    "url": "/documentation/section_page_layout#card"
  },
  {
    "title": "Page Layout: Column Element",
    "content": "Provides a container which arranges its child in a column.\n\n:param wrap: whether to wrap the content (default: `False`)\n:param align_items: alignment of the items in the column (\"start\", \"end\", \"center\", \"baseline\", or \"stretch\"; default: `None`)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.column():\n    ui.label('label 1')\n    ui.label('label 2')\n    ui.label('label 3')\n\nui.run()",
    "url": "/documentation/section_page_layout#column_element"
  },
  {
    "title": "Page Layout: Row Element",
    "content": "Provides a container which arranges its child in a row.\n\n:param wrap: whether to wrap the content (default: `True`)\n:param align_items: alignment of the items in the row (\"start\", \"end\", \"center\", \"baseline\", or \"stretch\"; default: `None`)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.row():\n    ui.label('label 1')\n    ui.label('label 2')\n    ui.label('label 3')\n\nui.run()",
    "url": "/documentation/section_page_layout#row_element"
  },
  {
    "title": "Page Layout: Grid Element",
    "content": "Provides a container which arranges its child in a grid.\n\n:param rows: number of rows in the grid or a string with the grid-template-rows CSS property (e.g. 'auto 1fr')\n:param columns: number of columns in the grid or a string with the grid-template-columns CSS property (e.g. 'auto 1fr')\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.grid(columns=2):\n    ui.label('Name:')\n    ui.label('Tom')\n\n    ui.label('Age:')\n    ui.label('42')\n\n    ui.label('Height:')\n    ui.label('1.80m')\n\nui.run()",
    "url": "/documentation/section_page_layout#grid_element"
  },
  {
    "title": "Page Layout: List",
    "content": "A list element based on Quasar's `QList \u003Chttps://quasar.dev/vue-components/list-and-list-items#qlist-api\u003E`_ component.\nIt provides a container for ``ui.item`` elements.\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.list().props('dense separator'):\n    ui.item('3 Apples')\n    ui.item('5 Bananas')\n    ui.item('8 Strawberries')\n    ui.item('13 Walnuts')\n\nui.run()",
    "url": "/documentation/section_page_layout#list"
  },
  {
    "title": "Page Layout: Slide Item",
    "content": "This element is based on Quasar's `QSlideItem \u003Chttps://quasar.dev/vue-components/slide-item/\u003E`_ component.\n\nIf the ``text`` parameter is provided, a nested ``ui.item`` element will be created with the given text.\nIf you want to customize how the text is displayed, you can place custom elements inside the slide item.\n\nTo fill slots for individual slide actions, use the ``left``, ``right``, ``top``, or ``bottom`` methods or\nthe ``action`` method with a side argument (\"left\", \"right\", \"top\", or \"bottom\").\n\nOnce a slide action has occurred, the slide item can be reset back to its initial state using the ``reset`` method.\n\n*Added in version 2.12.0*\n\n:param text: text to be displayed (default: \"\")\n:param on_slide: callback which is invoked when any slide action is activated\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.list().props('bordered separator'):\n    with ui.slide_item('Slide me left or right') as slide_item_1:\n        slide_item_1.left('Left', color='green')\n        slide_item_1.right('Right', color='red')\n    with ui.slide_item('Slide me up or down') as slide_item_2:\n        slide_item_2.top('Top', color='blue')\n        slide_item_2.bottom('Bottom', color='purple')\n\nui.run()",
    "url": "/documentation/section_page_layout#slide_item"
  },
  {
    "title": "Page Layout: Fullscreen control element",
    "content": "This element is based on Quasar's `AppFullscreen \u003Chttps://quasar.dev/quasar-plugins/app-fullscreen\u003E`_ plugin\nand provides a way to enter, exit and toggle the fullscreen mode.\n\nImportant notes:\n\n* Due to security reasons, the fullscreen mode can only be entered from a previous user interaction such as a button click.\n* The long-press escape requirement only works in some browsers like Google Chrome or Microsoft Edge.\n\n*Added in version 2.11.0*\n\n:param require_escape_hold: whether the user needs to long-press the escape key to exit fullscreen mode\n:param on_value_change: callback which is invoked when the fullscreen state changes\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nfullscreen = ui.fullscreen()\n\nui.button('Enter Fullscreen', on_click=fullscreen.enter)\nui.button('Exit Fullscreen', on_click=fullscreen.exit)\nui.button('Toggle Fullscreen', on_click=fullscreen.toggle)\n\nui.run()",
    "url": "/documentation/section_page_layout#fullscreen_control_element"
  },
  {
    "title": "Page Layout: Clear Containers",
    "content": "To remove all elements from a row, column or card container, use can call\n```py\ncontainer.clear()\n```\n\nAlternatively, you can remove individual elements by calling\n\n- `container.remove(element: Element)`,\n- `container.remove(index: int)`, or\n- `element.delete()`.",
    "format": "md",
    "demo": "from nicegui import ui\n\ncontainer = ui.row()\n\ndef add_face():\n    with container:\n        ui.icon('face')\nadd_face()\n\nui.button('Add', on_click=add_face)\nui.button('Remove', on_click=lambda: container.remove(0) if list(container) else None)\nui.button('Clear', on_click=container.clear)\n\nui.run()",
    "url": "/documentation/section_page_layout#clear_containers"
  },
  {
    "title": "Page Layout: Teleport",
    "content": "An element that allows us to transmit the content from within a component to any location on the page.\n\n:param to: NiceGUI element or CSS selector of the target element for the teleported content\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nmarkdown = ui.markdown('Enter your **name**!')\n\ndef inject_input():\n    with ui.teleport(f'#{markdown.html_id} strong'):\n        ui.input('name').classes('inline-flex').props('dense outlined')\n\nui.button('inject input', on_click=inject_input)\n\nui.run()",
    "url": "/documentation/section_page_layout#teleport"
  },
  {
    "title": "Page Layout: Expansion Element",
    "content": "Provides an expandable container based on Quasar's `QExpansionItem \u003Chttps://quasar.dev/vue-components/expansion-item\u003E`_ component.\n\n:param text: title text\n:param caption: optional caption (or sub-label) text\n:param icon: optional icon (default: None)\n:param group: optional group name for coordinated open/close state within the group a.k.a. \"accordion mode\"\n:param value: whether the expansion should be opened on creation (default: `False`)\n:param on_value_change: callback to execute when value changes\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.expansion('Expand!', icon='work').classes('w-full'):\n    ui.label('inside the expansion')\n\nui.run()",
    "url": "/documentation/section_page_layout#expansion_element"
  },
  {
    "title": "Page Layout: Scroll Area",
    "content": "A way of customizing the scrollbars by encapsulating your content.\nThis element exposes the Quasar `ScrollArea \u003Chttps://quasar.dev/vue-components/scroll-area/\u003E`_ component.\n\n:param on_scroll: function to be called when the scroll position changes\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.row():\n    with ui.scroll_area().classes('w-32 h-32 border'):\n        ui.label('I scroll. ' * 20)\n    with ui.column().classes('p-4 w-32 h-32 border'):\n        ui.label('I will not scroll. ' * 10)\n\nui.run()",
    "url": "/documentation/section_page_layout#scroll_area"
  },
  {
    "title": "Page Layout: Separator",
    "content": "This element is based on Quasar's `QSeparator \u003Chttps://quasar.dev/vue-components/separator\u003E`_ component.\n\nIt serves as a separator for cards, menus and other component containers and is similar to HTML's \u003Chr\u003E tag.\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.label('text above')\nui.separator()\nui.label('text below')\n\nui.run()",
    "url": "/documentation/section_page_layout#separator"
  },
  {
    "title": "Page Layout: Space",
    "content": "This element is based on Quasar's `QSpace \u003Chttps://quasar.dev/vue-components/space\u003E`_ component.\n\nIts purpose is to simply fill all available space inside of a flexbox element.\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.row().classes('w-full border'):\n    ui.label('Left')\n    ui.space()\n    ui.label('Right')\n\nui.run()",
    "url": "/documentation/section_page_layout#space"
  },
  {
    "title": "Page Layout: Skeleton",
    "content": "This element is based on Quasar's `QSkeleton \u003Chttps://quasar.dev/vue-components/skeleton\u003E`_ component.\nIt serves as a placeholder for loading content in cards, menus and other component containers.\nSee the `Quasar documentation \u003Chttps://quasar.dev/vue-components/skeleton/#predefined-types\u003E`_ for a list of available types.\n\n:param type: type of skeleton to display (default: \"rect\")\n:param tag: HTML tag to use for this element (default: \"div\")\n:param animation: animation effect of the skeleton placeholder (default: \"wave\")\n:param animation_speed: animation speed in seconds (default: 1.5)\n:param square: whether to remover border-radius so borders are squared (default: ``False``)\n:param bordered: whether to apply a default border to the component (default: ``False``)\n:param size: size in CSS units (overrides ``width`` and ``height``)\n:param width: width in CSS units (overridden by ``size`` if set)\n:param height: height in CSS units (overridden by ``size`` if set)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.skeleton().classes('w-full')\n\nui.run()",
    "url": "/documentation/section_page_layout#skeleton"
  },
  {
    "title": "Page Layout: Splitter",
    "content": "The `ui.splitter` element divides the screen space into resizable sections,\nallowing for flexible and responsive layouts in your application.\n\nBased on Quasar's Splitter component:\n`Splitter \u003Chttps://quasar.dev/vue-components/splitter\u003E`_\n\nIt provides three customizable slots, ``before``, ``after``, and ``separator``,\nwhich can be used to embed other elements within the splitter.\n\n:param horizontal: Whether to split horizontally instead of vertically\n:param limits: Two numbers representing the minimum and maximum split size of the two panels\n:param value: Size of the first panel (or second if using reverse)\n:param reverse: Whether to apply the model size to the second panel instead of the first\n:param on_change: callback which is invoked when the user releases the splitter\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.splitter() as splitter:\n    with splitter.before:\n        ui.label('This is some content on the left hand side.').classes('mr-2')\n    with splitter.after:\n        ui.label('This is some content on the right hand side.').classes('ml-2')\n\nui.run()",
    "url": "/documentation/section_page_layout#splitter"
  },
  {
    "title": "Page Layout: Tabs",
    "content": "The elements `ui.tabs`, `ui.tab`, `ui.tab_panels`, and `ui.tab_panel` resemble\n[Quasar's tabs](https://quasar.dev/vue-components/tabs) and\n[tab panels](https://quasar.dev/vue-components/tab-panels) API.\n\n`ui.tabs` creates a container for the tabs. This could be placed in a `ui.header` for example.\n`ui.tab_panels` creates a container for the tab panels with the actual content.\nEach `ui.tab_panel` is associated with a `ui.tab` element.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.tabs().classes('w-full') as tabs:\n    one = ui.tab('One')\n    two = ui.tab('Two')\nwith ui.tab_panels(tabs, value=two).classes('w-full'):\n    with ui.tab_panel(one):\n        ui.label('First tab')\n    with ui.tab_panel(two):\n        ui.label('Second tab')\n\nui.run()",
    "url": "/documentation/section_page_layout#tabs"
  },
  {
    "title": "Page Layout: Stepper",
    "content": "This element represents `Quasar's QStepper \u003Chttps://quasar.dev/vue-components/stepper#qstepper-api\u003E`_ component.\nIt contains individual steps.\n\nTo avoid issues with dynamic elements when switching steps,\nthis element uses Vue's `keep-alive \u003Chttps://vuejs.org/guide/built-ins/keep-alive.html\u003E`_ component.\nIf client-side performance is an issue, you can disable this feature.\n\n:param value: `ui.step` or name of the step to be initially selected (default: `None` meaning the first step)\n:param on_value_change: callback to be executed when the selected step changes\n:param keep_alive: whether to use Vue's keep-alive component on the content (default: `True`)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.stepper().props('vertical').classes('w-full') as stepper:\n    with ui.step('Preheat'):\n        ui.label('Preheat the oven to 350 degrees')\n        with ui.stepper_navigation():\n            ui.button('Next', on_click=stepper.next)\n    with ui.step('Ingredients'):\n        ui.label('Mix the ingredients')\n        with ui.stepper_navigation():\n            ui.button('Next', on_click=stepper.next)\n            ui.button('Back', on_click=stepper.previous).props('flat')\n    with ui.step('Bake'):\n        ui.label('Bake for 20 minutes')\n        with ui.stepper_navigation():\n            ui.button('Done', on_click=lambda: ui.notify('Yay!', type='positive'))\n            ui.button('Back', on_click=stepper.previous).props('flat')\n\nui.run()",
    "url": "/documentation/section_page_layout#stepper"
  },
  {
    "title": "Page Layout: Timeline",
    "content": "This element represents `Quasar's QTimeline \u003Chttps://quasar.dev/vue-components/timeline#qtimeline-api\u003E`_ component.\n\n:param side: Side (\"left\" or \"right\"; default: \"left\").\n:param layout: Layout (\"dense\", \"comfortable\" or \"loose\"; default: \"dense\").\n:param color: Color of the icons.\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.timeline(side='right'):\n    ui.timeline_entry('Rodja and Falko start working on NiceGUI.',\n                      title='Initial commit',\n                      subtitle='May 07, 2021')\n    ui.timeline_entry('The first PyPI package is released.',\n                      title='Release of 0.1',\n                      subtitle='May 14, 2021')\n    ui.timeline_entry('Large parts are rewritten to remove JustPy '\n                      'and to upgrade to Vue 3 and Quasar 2.',\n                      title='Release of 1.0',\n                      subtitle='December 15, 2022',\n                      icon='rocket')\n\nui.run()",
    "url": "/documentation/section_page_layout#timeline"
  },
  {
    "title": "Page Layout: Carousel",
    "content": "This element represents `Quasar's QCarousel \u003Chttps://quasar.dev/vue-components/carousel#qcarousel-api\u003E`_ component.\nIt contains individual carousel slides.\n\n:param value: `ui.carousel_slide` or name of the slide to be initially selected (default: `None` meaning the first slide)\n:param on_value_change: callback to be executed when the selected slide changes\n:param animated: whether to animate slide transitions (default: `False`)\n:param arrows: whether to show arrows for manual slide navigation (default: `False`)\n:param navigation: whether to show navigation dots for manual slide navigation (default: `False`)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.carousel(animated=True, arrows=True, navigation=True).props('height=180px'):\n    with ui.carousel_slide().classes('p-0'):\n        ui.image('https://picsum.photos/id/30/270/180').classes('w-[270px]')\n    with ui.carousel_slide().classes('p-0'):\n        ui.image('https://picsum.photos/id/31/270/180').classes('w-[270px]')\n    with ui.carousel_slide().classes('p-0'):\n        ui.image('https://picsum.photos/id/32/270/180').classes('w-[270px]')\n\nui.run()",
    "url": "/documentation/section_page_layout#carousel"
  },
  {
    "title": "Page Layout: Pagination",
    "content": "A pagination element wrapping Quasar's `QPagination \u003Chttps://quasar.dev/vue-components/pagination\u003E`_ component.\n\n:param min: minimum page number\n:param max: maximum page number\n:param direction_links: whether to show first/last page links\n:param value: initial page (defaults to `min` if no value is provided)\n:param on_change: callback to be invoked when the value changes\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\np = ui.pagination(1, 5, direction_links=True)\nui.label().bind_text_from(p, 'value', lambda v: f'Page {v}')\n\nui.run()",
    "url": "/documentation/section_page_layout#pagination"
  },
  {
    "title": "Page Layout: Menu",
    "content": "Creates a menu based on Quasar's `QMenu \u003Chttps://quasar.dev/vue-components/menu\u003E`_ component.\nThe menu should be placed inside the element where it should be shown.\n\nAdvanced tip:\nUse the `auto-close` prop to automatically close the menu on any click event directly without a server round-trip.\n\n:param value: whether the menu is already opened (default: `False`)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.row().classes('w-full items-center'):\n    result = ui.label().classes('mr-auto')\n    with ui.button(icon='menu'):\n        with ui.menu() as menu:\n            ui.menu_item('Menu item 1', lambda: result.set_text('Selected item 1'))\n            ui.menu_item('Menu item 2', lambda: result.set_text('Selected item 2'))\n            ui.menu_item('Menu item 3 (keep open)',\n                         lambda: result.set_text('Selected item 3'), auto_close=False)\n            ui.separator()\n            ui.menu_item('Close', menu.close)\n\nui.run()",
    "url": "/documentation/section_page_layout#menu"
  },
  {
    "title": "Page Layout: Context Menu",
    "content": "Creates a context menu based on Quasar's `QMenu \u003Chttps://quasar.dev/vue-components/menu\u003E`_ component.\nThe context menu should be placed inside the element where it should be shown.\nIt is automatically opened when the user right-clicks on the element and appears at the mouse position.\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.image('https://picsum.photos/id/377/640/360'):\n    with ui.context_menu():\n        ui.menu_item('Flip horizontally')\n        ui.menu_item('Flip vertically')\n        ui.separator()\n        ui.menu_item('Reset', auto_close=False)\n\nui.run()",
    "url": "/documentation/section_page_layout#context_menu"
  },
  {
    "title": "Page Layout: Tooltip",
    "content": "This element is based on Quasar's `QTooltip \u003Chttps://quasar.dev/vue-components/tooltip\u003E`_ component.\nIt can be placed in another element to show additional information on hover.\n\nInstead of passing a string as the first argument, you can also nest other elements inside the tooltip.\n\n:param text: the content of the tooltip (default: '')\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.button(icon='thumb_up'):\n    ui.tooltip('I like this').classes('bg-green')\n\nui.run()",
    "url": "/documentation/section_page_layout#tooltip"
  },
  {
    "title": "Page Layout: Notification",
    "content": "Displays a notification on the screen.\n\n:param message: content of the notification\n:param position: position on the screen (\"top-left\", \"top-right\", \"bottom-left\", \"bottom-right\", \"top\", \"bottom\", \"left\", \"right\" or \"center\", default: \"bottom\")\n:param close_button: optional label of a button to dismiss the notification (default: `False`)\n:param type: optional type (\"positive\", \"negative\", \"warning\", \"info\" or \"ongoing\")\n:param color: optional color name\n:param multi_line: enable multi-line notifications\n\nNote: You can pass additional keyword arguments according to `Quasar's Notify API \u003Chttps://quasar.dev/quasar-plugins/notify#notify-api\u003E`_.\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.button('Say hi!', on_click=lambda: ui.notify('Hi!', close_button='OK'))\n\nui.run()",
    "url": "/documentation/section_page_layout#notification"
  },
  {
    "title": "Page Layout: Notification element",
    "content": "Displays a notification on the screen.\nIn contrast to `ui.notify`, this element allows to update the notification message and other properties once the notification is displayed.\nThe notification can be removed with `dismiss()`.\n\n:param message: content of the notification\n:param position: position on the screen (\"top-left\", \"top-right\", \"bottom-left\", \"bottom-right\", \"top\", \"bottom\", \"left\", \"right\" or \"center\", default: \"bottom\")\n:param close_button: optional label of a button to dismiss the notification (default: `False`)\n:param type: optional type (\"positive\", \"negative\", \"warning\", \"info\" or \"ongoing\")\n:param color: optional color name\n:param multi_line: enable multi-line notifications\n:param icon: optional name of an icon to be displayed in the notification (default: `None`)\n:param spinner: display a spinner in the notification (default: False)\n:param timeout: optional timeout in seconds after which the notification is dismissed (default: 5.0)\n:param on_dismiss: optional callback to be invoked when the notification is dismissed\n:param options: optional dictionary with all options (overrides all other arguments)\n\nNote: You can pass additional keyword arguments according to `Quasar's Notify API \u003Chttps://quasar.dev/quasar-plugins/notify#notify-api\u003E`_.\n",
    "format": "rst",
    "demo": "import asyncio\nfrom nicegui import ui\n\nasync def compute():\n    n = ui.notification(timeout=None)\n    for i in range(10):\n        n.message = f'Computing {i/10:.0%}'\n        n.spinner = True\n        await asyncio.sleep(0.2)\n    n.message = 'Done!'\n    n.spinner = False\n    await asyncio.sleep(1)\n    n.dismiss()\n\nui.button('Compute', on_click=compute)\n\nui.run()",
    "url": "/documentation/section_page_layout#notification_element"
  },
  {
    "title": "Page Layout: Dialog",
    "content": "Creates a dialog based on Quasar's `QDialog \u003Chttps://quasar.dev/vue-components/dialog\u003E`_ component.\nBy default it is dismissible by clicking or pressing ESC.\nTo make it persistent, set `.props('persistent')` on the dialog element.\n\nNOTE: The dialog is an element.\nThat means it is not removed when closed, but only hidden.\nYou should either create it only once and then reuse it, or remove it with `.clear()` after dismissal.\n\n:param value: whether the dialog should be opened on creation (default: `False`)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.dialog() as dialog, ui.card():\n    ui.label('Hello world!')\n    ui.button('Close', on_click=dialog.close)\n\nui.button('Open a dialog', on_click=dialog.open)\n\nui.run()",
    "url": "/documentation/section_page_layout#dialog"
  },
  {
    "title": "ui.download: Download functions",
    "content": "These functions allow you to download files, URLs or raw data.\n\n*Added in version 2.14.0*\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.button('Local file', on_click=lambda: ui.download.file('main.py'))\nui.button('From URL', on_click=lambda: ui.download.from_url('/logo.png'))\nui.button('Content', on_click=lambda: ui.download.content('Hello World', 'hello.txt'))\n\nui.run()",
    "url": "/documentation/download#download_functions"
  },
  {
    "title": "ui.download: Download from a relative URL",
    "content": "Function to trigger the download from a relative URL.\n\nNote:\nThis function is intended to be used with relative URLs only.\nFor absolute URLs, the browser ignores the download instruction and tries to view the file in a new tab\nif possible, such as images, PDFs, etc.\nTherefore, the download may only work for some file types such as .zip, .db, etc.\nFurthermore, the browser ignores filename and media_type parameters,\nrespecting the origin server's headers instead.\nEither replace the absolute URL with a relative one, or use ``ui.navigate.to(url, new_tab=True)`` instead.\n\n*Added in version 2.14.0*\n\n*Updated in version 2.19.0: Added warning for cross-origin downloads*\n\n:param url: URL\n:param filename: name of the file to download (default: name of the file on the server)\n:param media_type: media type of the file to download (default: \"\")\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.button('Download', on_click=lambda: ui.download.from_url('/logo.png'))\n\nui.run()",
    "url": "/documentation/download#download_from_a_relative_url"
  },
  {
    "title": "ui.download: Download raw bytes or string content",
    "content": "Function to trigger the download of raw data.\n\n*Added in version 2.14.0*\n\n:param content: raw bytes or string\n:param filename: name of the file to download (default: name of the file on the server)\n:param media_type: media type of the file to download (default: \"\")\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.button('Download', on_click=lambda: ui.download.content('Hello World', 'hello.txt'))\n\nui.run()",
    "url": "/documentation/download#download_raw_bytes_or_string_content"
  },
  {
    "title": "ui.download: Download file from local path",
    "content": "Function to trigger the download of a file.\n\n*Added in version 2.14.0*\n\n:param path: local path of the file\n:param filename: name of the file to download (default: name of the file on the server)\n:param media_type: media type of the file to download (default: \"\")\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.button('Download', on_click=lambda: ui.download.file('main.py'))\n\nui.run()",
    "url": "/documentation/download#download_file_from_local_path"
  },
  {
    "title": "ui.navigate: Navigation functions",
    "content": "These functions allow you to navigate within the browser history and to external URLs.\n\n*Added in version 2.0.0*\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.row():\n    ui.button('Back', on_click=ui.navigate.back)\n    ui.button('Forward', on_click=ui.navigate.forward)\n    ui.button('Reload', on_click=ui.navigate.reload)\n    ui.button(icon='savings',\n              on_click=lambda: ui.navigate.to('https://github.com/sponsors/zauberzeug'))\n\nui.run()",
    "url": "/documentation/navigate#navigation_functions"
  },
  {
    "title": "ui.navigate: ui.navigate.to (formerly ui.open)",
    "content": "Can be used to programmatically open a different page or URL.\n\nWhen using the `new_tab` parameter, the browser might block the new tab.\nThis is a browser setting and cannot be changed by the application.\nYou might want to use `ui.link` and its `new_tab` parameter instead.\n\nThis functionality was previously available as `ui.open` which is now deprecated.\n\nNote: When using an `auto-index page \u003C/documentation/section_pages_routing#auto-index_page\u003E`_ (e.g. no `@page` decorator),\nall clients (i.e. browsers) connected to the page will open the target URL unless a socket is specified.\n\n:param target: page function, NiceGUI element on the same page or string that is a an absolute URL or relative path from base URL\n:param new_tab: whether to open the target in a new tab (might be blocked by the browser)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nurl = 'https://github.com/zauberzeug/nicegui/'\nui.button('Open GitHub', on_click=lambda: ui.navigate.to(url, new_tab=True))\n\nui.run()",
    "url": "/documentation/navigate#ui_navigate_to_(formerly_ui_open)"
  },
  {
    "title": "ui.navigate: Push and replace URLs",
    "content": "The `history` API allows you to push and replace URLs to the browser history.\n\nWhile the `history.push` method pushes a new URL to the history,\nthe `history.replace` method replaces the current URL.\n\nSee [JavaScript's History API](https://developer.mozilla.org/en-US/docs/Web/API/History) for more information.\n\n*Added in version 2.13.0*",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.button('Push URL', on_click=lambda: ui.navigate.history.push('/a'))\nui.button('Replace URL', on_click=lambda: ui.navigate.history.replace('/b'))\n\nui.run()",
    "url": "/documentation/navigate#push_and_replace_urls"
  },
  {
    "title": "ui.page: Page",
    "content": "This decorator marks a function to be a page builder.\nEach user accessing the given route will see a new instance of the page.\nThis means it is private to the user and not shared with others\n(as it is done `when placing elements outside of a page decorator \u003Chttps://nicegui.io/documentation/section_pages_routing#auto-index_page\u003E`_).\n\nNotes:\n\n- The name of the decorated function is unused and can be anything.\n- The page route is determined by the `path` argument and registered globally.\n- The decorator does only work for free functions and static methods.\n  Instance methods or initializers would require a `self` argument, which the router cannot associate.\n  See `our modularization example \u003Chttps://github.com/zauberzeug/nicegui/tree/main/examples/modularization/\u003E`_\n  for strategies to structure your code.\n\n:param path: route of the new page (path must start with '/')\n:param title: optional page title\n:param viewport: optional viewport meta tag content\n:param favicon: optional relative filepath or absolute URL to a favicon (default: `None`, NiceGUI icon will be used)\n:param dark: whether to use Quasar's dark mode (defaults to `dark` argument of `run` command)\n:param language: language of the page (defaults to `language` argument of `run` command)\n:param response_timeout: maximum time for the decorated function to build the page (default: 3.0 seconds)\n:param reconnect_timeout: maximum time the server waits for the browser to reconnect (defaults to `reconnect_timeout` argument of `run` command))\n:param api_router: APIRouter instance to use, can be left `None` to use the default\n:param kwargs: additional keyword arguments passed to FastAPI's @app.get method\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\n@ui.page('/other_page')\ndef other_page():\n    ui.label('Welcome to the other side')\n\n@ui.page('/dark_page', dark=True)\ndef dark_page():\n    ui.label('Welcome to the dark side')\n\nui.link('Visit other page', other_page)\nui.link('Visit dark page', dark_page)\n\nui.run()",
    "url": "/documentation/page#page"
  },
  {
    "title": "ui.page: Pages with Path Parameters",
    "content": "Page routes can contain parameters like [FastAPI](https://fastapi.tiangolo.com/tutorial/path-params/).\nIf type-annotated, they are automatically converted to bool, int, float and complex values.\nIf the page function expects a `request` argument, the request object is automatically provided.\nThe `client` argument provides access to the websocket connection, layout, etc.",
    "format": "md",
    "demo": "from nicegui import ui\n\n@ui.page('/repeat/{word}/{count}')\ndef page(word: str, count: int):\n    ui.label(word * count)\n\nui.link('Say hi to Santa!', '/repeat/Ho! /3')\n\nui.run()",
    "url": "/documentation/page#pages_with_path_parameters"
  },
  {
    "title": "ui.page: Wait for Client Connection",
    "content": "To wait for a client connection, you can add a `client` argument to the decorated page function\nand await `client.connected()`.\nAll code below that statement is executed after the websocket connection between server and client has been established.\n\nFor example, this allows you to run JavaScript commands; which is only possible with a client connection (see [#112](https://github.com/zauberzeug/nicegui/issues/112)).\nAlso it is possible to do async stuff while the user already sees some content.",
    "format": "md",
    "demo": "import asyncio\nfrom nicegui import ui\n\n@ui.page('/wait_for_connection')\nasync def wait_for_connection():\n    ui.label('This text is displayed immediately.')\n    await ui.context.client.connected()\n    await asyncio.sleep(2)\n    ui.label('This text is displayed 2 seconds after the page has been fully loaded.')\n\nui.link('wait for connection', wait_for_connection)\n\nui.run()",
    "url": "/documentation/page#wait_for_client_connection"
  },
  {
    "title": "ui.page: Multicasting",
    "content": "The content on a page is private to the client (the browser tab) and has its own local element context.\nIf you want to send updates to _all_ clients of a specific page, you can use the `app.clients` iterator.\nThis is useful for modifying UI elements from a background process or from other pages.\n\n*Added in version 2.7.0*",
    "format": "md",
    "demo": "from nicegui import app, ui\n\n@ui.page('/multicast_receiver')\ndef page():\n    ui.label('This page will show messages from the index page.')\n\ndef send(message: str):\n    for client in app.clients('/multicast_receiver'):\n        with client:\n            ui.notify(message)\n\nui.button('Send message', on_click=lambda: send('Hi!'))\nui.link('Open receiver', '/multicast_receiver', new_tab=True)\n\nui.run()",
    "url": "/documentation/page#multicasting"
  },
  {
    "title": "ui.page: Modularize with APIRouter",
    "content": "You can use the NiceGUI specialization of\n[FastAPI's APIRouter](https://fastapi.tiangolo.com/tutorial/bigger-applications/?h=apirouter#apirouter)\nto modularize your code by grouping pages and other routes together.\nThis is especially useful if you want to reuse the same prefix for multiple pages.\nThe router and its pages can be neatly tugged away in a separate module (e.g. file) and\nthe router is simply imported and included in the main app.\nSee our [modularization example](https://github.com/zauberzeug/nicegui/blob/main/examples/modularization/api_router_example.py)\nfor a multi-file app structure using an API router.",
    "format": "md",
    "demo": "from nicegui import APIRouter, app, ui\n\nrouter = APIRouter(prefix='/sub-path')\n\n@router.page('/')\ndef page():\n    ui.label('This is content on /sub-path')\n\n@router.page('/sub-sub-path')\ndef page():\n    ui.label('This is content on /sub-path/sub-sub-path')\n\nui.link('Visit sub-path', '/sub-path')\nui.link('Visit sub-sub-path', '/sub-path/sub-sub-path')\n\napp.include_router(router)\n\nui.run()",
    "url": "/documentation/page#modularize_with_apirouter"
  },
  {
    "title": "Page Layout: Page Layout",
    "content": "With `ui.header`, `ui.footer`, `ui.left_drawer` and `ui.right_drawer` you can add additional layout elements to a page.\nThe `fixed` argument controls whether the element should scroll or stay fixed on the screen.\nThe `top_corner` and `bottom_corner` arguments indicate whether a drawer should expand to the top or bottom of the page.\nSee \u003Chttps://quasar.dev/layout/header-and-footer\u003E and \u003Chttps://quasar.dev/layout/drawer\u003E for more information about possible props.\nWith `ui.page_sticky` you can place an element \"sticky\" on the screen.\nSee \u003Chttps://quasar.dev/layout/page-sticky\u003E for more information.",
    "format": "md",
    "demo": "from nicegui import ui\n\n@ui.page('/page_layout')\ndef page_layout():\n    ui.label('CONTENT')\n    [ui.label(f'Line {i}') for i in range(100)]\n    with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):\n        ui.label('HEADER')\n        ui.button(on_click=lambda: right_drawer.toggle(), icon='menu').props('flat color=white')\n    with ui.left_drawer(top_corner=True, bottom_corner=True).style('background-color: #d7e3f4'):\n        ui.label('LEFT DRAWER')\n    with ui.right_drawer(fixed=False).style('background-color: #ebf1fa').props('bordered') as right_drawer:\n        ui.label('RIGHT DRAWER')\n    with ui.footer().style('background-color: #3874c8'):\n        ui.label('FOOTER')\n\nui.link('show page with fancy layout', page_layout)\n\nui.run()",
    "url": "/documentation/page_layout#page_layout"
  },
  {
    "title": "Page Layout: Reference for ui.header",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/page_layout#reference_for_ui_header"
  },
  {
    "title": "Page Layout: Reference for ui.left_drawer",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/page_layout#reference_for_ui_left_drawer"
  },
  {
    "title": "Page Layout: Reference for ui.right_drawer",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/page_layout#reference_for_ui_right_drawer"
  },
  {
    "title": "Page Layout: Reference for ui.footer",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/page_layout#reference_for_ui_footer"
  },
  {
    "title": "Page Layout: Reference for ui.page_sticky",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/page_layout#reference_for_ui_page_sticky"
  },
  {
    "title": "ui.page_title: Page title",
    "content": "Set the page title for the current client.\n\n:param title: page title\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.button('Change page title', on_click=lambda: ui.page_title('New Title'))\n\nui.run()",
    "url": "/documentation/page_title#page_title"
  },
  {
    "title": "Pages & Routing: Page",
    "content": "This decorator marks a function to be a page builder.\nEach user accessing the given route will see a new instance of the page.\nThis means it is private to the user and not shared with others\n(as it is done `when placing elements outside of a page decorator \u003Chttps://nicegui.io/documentation/section_pages_routing#auto-index_page\u003E`_).\n\nNotes:\n\n- The name of the decorated function is unused and can be anything.\n- The page route is determined by the `path` argument and registered globally.\n- The decorator does only work for free functions and static methods.\n  Instance methods or initializers would require a `self` argument, which the router cannot associate.\n  See `our modularization example \u003Chttps://github.com/zauberzeug/nicegui/tree/main/examples/modularization/\u003E`_\n  for strategies to structure your code.\n\n:param path: route of the new page (path must start with '/')\n:param title: optional page title\n:param viewport: optional viewport meta tag content\n:param favicon: optional relative filepath or absolute URL to a favicon (default: `None`, NiceGUI icon will be used)\n:param dark: whether to use Quasar's dark mode (defaults to `dark` argument of `run` command)\n:param language: language of the page (defaults to `language` argument of `run` command)\n:param response_timeout: maximum time for the decorated function to build the page (default: 3.0 seconds)\n:param reconnect_timeout: maximum time the server waits for the browser to reconnect (defaults to `reconnect_timeout` argument of `run` command))\n:param api_router: APIRouter instance to use, can be left `None` to use the default\n:param kwargs: additional keyword arguments passed to FastAPI's @app.get method\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\n@ui.page('/other_page')\ndef other_page():\n    ui.label('Welcome to the other side')\n\n@ui.page('/dark_page', dark=True)\ndef dark_page():\n    ui.label('Welcome to the dark side')\n\nui.link('Visit other page', other_page)\nui.link('Visit dark page', dark_page)\n\nui.run()",
    "url": "/documentation/section_pages_routing#page"
  },
  {
    "title": "Pages & Routing: Auto-index page",
    "content": "Pages created with the `@ui.page` decorator are \"private\".\nTheir content is re-created for each client.\nThus, in the demo to the right, the displayed ID on the private page changes when the browser reloads the page.\n\nUI elements that are not wrapped in a decorated page function are placed on an automatically generated index page at route \"/\".\nThis auto-index page is created once on startup and *shared* across all clients that might connect.\nThus, each connected client will see the *same* elements.\nIn the demo to the right, the displayed ID on the auto-index page remains constant when the browser reloads the page.",
    "format": "md",
    "demo": "from nicegui import ui\nfrom uuid import uuid4\n\n@ui.page('/private_page')\nasync def private_page():\n    ui.label(f'private page with ID {uuid4()}')\n\nui.label(f'shared auto-index page with ID {uuid4()}')\nui.link('private page', private_page)\n\nui.run()",
    "url": "/documentation/section_pages_routing#auto-index_page"
  },
  {
    "title": "Pages & Routing: Page Layout",
    "content": "With `ui.header`, `ui.footer`, `ui.left_drawer` and `ui.right_drawer` you can add additional layout elements to a page.\nThe `fixed` argument controls whether the element should scroll or stay fixed on the screen.\nThe `top_corner` and `bottom_corner` arguments indicate whether a drawer should expand to the top or bottom of the page.\nSee \u003Chttps://quasar.dev/layout/header-and-footer\u003E and \u003Chttps://quasar.dev/layout/drawer\u003E for more information about possible props.\nWith `ui.page_sticky` you can place an element \"sticky\" on the screen.\nSee \u003Chttps://quasar.dev/layout/page-sticky\u003E for more information.",
    "format": "md",
    "demo": "from nicegui import ui\n\n@ui.page('/page_layout')\ndef page_layout():\n    ui.label('CONTENT')\n    [ui.label(f'Line {i}') for i in range(100)]\n    with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):\n        ui.label('HEADER')\n        ui.button(on_click=lambda: right_drawer.toggle(), icon='menu').props('flat color=white')\n    with ui.left_drawer(top_corner=True, bottom_corner=True).style('background-color: #d7e3f4'):\n        ui.label('LEFT DRAWER')\n    with ui.right_drawer(fixed=False).style('background-color: #ebf1fa').props('bordered') as right_drawer:\n        ui.label('RIGHT DRAWER')\n    with ui.footer().style('background-color: #3874c8'):\n        ui.label('FOOTER')\n\nui.link('show page with fancy layout', page_layout)\n\nui.run()",
    "url": "/documentation/section_pages_routing#page_layout"
  },
  {
    "title": "Pages & Routing: Parameter injection",
    "content": "Thanks to FastAPI, a page function accepts optional parameters to provide\n[path parameters](https://fastapi.tiangolo.com/tutorial/path-params/),\n[query parameters](https://fastapi.tiangolo.com/tutorial/query-params/) or the whole incoming\n[request](https://fastapi.tiangolo.com/advanced/using-request-directly/) for accessing\nthe body payload, headers, cookies and more.",
    "format": "md",
    "demo": "from nicegui import ui\n\n@ui.page('/icon/{icon}')\ndef icons(icon: str, amount: int = 1):\n    ui.label(icon).classes('text-h3')\n    with ui.row():\n        [ui.icon(icon).classes('text-h3') for _ in range(amount)]\nui.link('Star', '/icon/star?amount=5')\nui.link('Home', '/icon/home')\nui.link('Water', '/icon/water_drop?amount=3')\n\nui.run()",
    "url": "/documentation/section_pages_routing#parameter_injection"
  },
  {
    "title": "Pages & Routing: Page title",
    "content": "Set the page title for the current client.\n\n:param title: page title\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.button('Change page title', on_click=lambda: ui.page_title('New Title'))\n\nui.run()",
    "url": "/documentation/section_pages_routing#page_title"
  },
  {
    "title": "Pages & Routing: Navigation functions",
    "content": "These functions allow you to navigate within the browser history and to external URLs.\n\n*Added in version 2.0.0*\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.row():\n    ui.button('Back', on_click=ui.navigate.back)\n    ui.button('Forward', on_click=ui.navigate.forward)\n    ui.button('Reload', on_click=ui.navigate.reload)\n    ui.button(icon='savings',\n              on_click=lambda: ui.navigate.to('https://github.com/sponsors/zauberzeug'))\n\nui.run()",
    "url": "/documentation/section_pages_routing#navigation_functions"
  },
  {
    "title": "Pages & Routing: ui.open",
    "content": "\n    The `ui.open` function is deprecated.\n    Use [`ui.navigate.to`](navigate#ui_navigate_to_(formerly_ui_open)) instead.\n",
    "format": "md",
    "demo": "",
    "url": "/documentation/section_pages_routing#ui_open"
  },
  {
    "title": "Pages & Routing: Download functions",
    "content": "These functions allow you to download files, URLs or raw data.\n\n*Added in version 2.14.0*\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.button('Local file', on_click=lambda: ui.download.file('main.py'))\nui.button('From URL', on_click=lambda: ui.download.from_url('/logo.png'))\nui.button('Content', on_click=lambda: ui.download.content('Hello World', 'hello.txt'))\n\nui.run()",
    "url": "/documentation/section_pages_routing#download_functions"
  },
  {
    "title": "Pages & Routing: Add a directory of static files",
    "content": "`add_static_files()` makes a local directory available at the specified endpoint, e.g. `'/static'`.\nThis is useful for providing local data like images to the frontend.\nOtherwise the browser would not be able to access the files.\nDo only put non-security-critical files in there, as they are accessible to everyone.\n\nTo make a single file accessible, you can use `add_static_file()`.\nFor media files which should be streamed, you can use `add_media_files()` or `add_media_file()` instead.\n\n:param url_path: string that starts with a slash \"/\" and identifies the path at which the files should be served\n:param local_directory: local folder with files to serve as static content\n:param follow_symlink: whether to follow symlinks (default: False)\n:param max_cache_age: value for max-age set in Cache-Control header (*added in version 2.8.0*)\n",
    "format": "rst",
    "demo": "from nicegui import app, ui\n\napp.add_static_files('/examples', 'examples')\nui.label('Some NiceGUI Examples').classes('text-h5')\nui.link('AI interface', '/examples/ai_interface/main.py')\nui.link('Custom FastAPI app', '/examples/fastapi/main.py')\nui.link('Authentication', '/examples/authentication/main.py')\n\nui.run()",
    "url": "/documentation/section_pages_routing#add_a_directory_of_static_files"
  },
  {
    "title": "Pages & Routing: Add directory of media files",
    "content": "`add_media_files()` allows a local files to be streamed from a specified endpoint, e.g. `'/media'`.\nThis should be used for media files to support proper streaming.\nOtherwise the browser would not be able to access and load the the files incrementally or jump to different positions in the stream.\nDo only put non-security-critical files in there, as they are accessible to everyone.\n\nTo make a single file accessible via streaming, you can use `add_media_file()`.\nFor small static files, you can use `add_static_files()` or `add_static_file()` instead.\n\n:param url_path: string that starts with a slash \"/\" and identifies the path at which the files should be served\n:param local_directory: local folder with files to serve as media content\n",
    "format": "rst",
    "demo": "import httpx\nfrom nicegui import app, ui\nfrom pathlib import Path\n\nmedia = Path('media')\nmedia.mkdir(exist_ok=True)\nr = httpx.get('https://cdn.coverr.co/videos/coverr-cloudy-sky-2765/1080p.mp4')\n(media  / 'clouds.mp4').write_bytes(r.content)\napp.add_media_files('/my_videos', media)\nui.video('/my_videos/clouds.mp4')\n\nui.run()",
    "url": "/documentation/section_pages_routing#add_directory_of_media_files"
  },
  {
    "title": "Pages & Routing: Add HTML to the page",
    "content": "You can add HTML to the page by calling `ui.add_head_html` or `ui.add_body_html`.\nThis is useful for adding custom CSS styles or JavaScript code.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.add_head_html('''\n    \u003Cstyle\u003E\n        .my-red-label {\n            color: Crimson;\n            font-weight: bold;\n        }\n    \u003C/style\u003E\n''')\nui.label('RED').classes('my-red-label')\n\nui.run()",
    "url": "/documentation/section_pages_routing#add_html_to_the_page"
  },
  {
    "title": "Pages & Routing: API Responses",
    "content": "NiceGUI is based on [FastAPI](https://fastapi.tiangolo.com/).\nThis means you can use all of FastAPI's features.\nFor example, you can implement a RESTful API in addition to your graphical user interface.\nYou simply import the `app` object from `nicegui`.\nOr you can run NiceGUI on top of your own FastAPI app by using `ui.run_with(app)` instead of starting a server automatically with `ui.run()`.\n\nYou can also return any other FastAPI response object inside a page function.\nFor example, you can return a `RedirectResponse` to redirect the user to another page if certain conditions are met.\nThis is used in our [authentication demo](https://github.com/zauberzeug/nicegui/tree/main/examples/authentication/main.py).",
    "format": "md",
    "demo": "import random\nfrom nicegui import app, ui\n\n@app.get('/random/{max}')\ndef generate_random_number(max: int):\n    return {'min': 0, 'max': max, 'value': random.randint(0, max)}\n\nmax = ui.number('max', value=100)\nui.button('generate random number',\n          on_click=lambda: ui.navigate.to(f'/random/{max.value:.0f}'))\n\nui.run()",
    "url": "/documentation/section_pages_routing#api_responses"
  },
  {
    "title": "ui.add_css: Add CSS style definitions to the page",
    "content": "This function can be used to add CSS style definitions to the head of the HTML page.\n\n*Added in version 2.0.0*\n\n:param content: CSS content (string or file path)\n:param shared: whether to add the code to all pages (default: ``False``, *added in version 2.14.0*)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.add_css('''\n    .red {\n        color: red;\n    }\n''')\nui.label('This is red with CSS.').classes('red')\n\nui.run()",
    "url": "/documentation/add_style#add_css_style_definitions_to_the_page"
  },
  {
    "title": "ui.add_css: Add SCSS style definitions to the page",
    "content": "This function can be used to add SCSS style definitions to the head of the HTML page.\n\n*Added in version 2.0.0*\n\n:param content: SCSS content (string or file path)\n:param indented: whether the content is indented (SASS) or not (SCSS) (default: `False`)\n:param shared: whether to add the code to all pages (default: ``False``, *added in version 2.14.0*)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.add_scss('''\n    .green {\n        background-color: lightgreen;\n        .blue {\n            color: blue;\n        }\n    }\n''')\nwith ui.element().classes('green'):\n    ui.label('This is blue on green with SCSS.').classes('blue')\n\nui.run()",
    "url": "/documentation/add_style#add_scss_style_definitions_to_the_page"
  },
  {
    "title": "ui.add_css: Add SASS style definitions to the page",
    "content": "This function can be used to add SASS style definitions to the head of the HTML page.\n\n*Added in version 2.0.0*\n\n:param content: SASS content (string or file path)\n:param shared: whether to add the code to all pages (default: ``False``, *added in version 2.14.0*)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.add_sass('''\n    .yellow\n        background-color: yellow\n        .purple\n            color: purple\n''')\nwith ui.element().classes('yellow'):\n    ui.label('This is purple on yellow with SASS.').classes('purple')\n\nui.run()",
    "url": "/documentation/add_style#add_sass_style_definitions_to_the_page"
  },
  {
    "title": "ui.colors: Color Theming",
    "content": "Sets the main colors (primary, secondary, accent, ...) used by `Quasar \u003Chttps://quasar.dev/style/theme-builder\u003E`_.\n\n:param primary: Primary color (default: \"#5898d4\")\n:param secondary: Secondary color (default: \"#26a69a\")\n:param accent: Accent color (default: \"#9c27b0\")\n:param dark: Dark color (default: \"#1d1d1d\")\n:param dark_page: Dark page color (default: \"#121212\")\n:param positive: Positive color (default: \"#21ba45\")\n:param negative: Negative color (default: \"#c10015\")\n:param info: Info color (default: \"#31ccec\")\n:param warning: Warning color (default: \"#f2c037\")\n:param custom_colors: Custom color definitions for branding (needs ``ui.colors`` to be called before custom color is ever used, *added in version 2.2.0*)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.button('Default', on_click=lambda: ui.colors())\nui.button('Gray', on_click=lambda: ui.colors(primary='#555'))\n\nui.run()",
    "url": "/documentation/colors#color_theming"
  },
  {
    "title": "ui.colors: Custom colors",
    "content": "You can add custom color definitions for branding.\nIn this case, `ui.colors` must be called before the custom color is ever used.\n\n*Added in version 2.2.0*",
    "format": "md",
    "demo": "from nicegui import ui\nfrom random import randint\n\nui.colors(brand='#424242')\nui.label('This is your custom brand color').classes('text-brand')\nui.button('Randomize', color='brand',\n          on_click=lambda: ui.colors(brand=f'#{randint(0, 0xffffff):06x}'))\n\nui.run()",
    "url": "/documentation/colors#custom_colors"
  },
  {
    "title": "ui.colors: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/colors#reference"
  },
  {
    "title": "ui.dark_mode: Dark mode",
    "content": "You can use this element to enable, disable or toggle dark mode on the page.\nThe value `None` represents auto mode, which uses the client's system preference.\n\nNote that this element overrides the `dark` parameter of the `ui.run` function and page decorators.\n\n:param value: Whether dark mode is enabled. If None, dark mode is set to auto.\n:param on_change: Callback that is invoked when the value changes.\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\ndark = ui.dark_mode()\nui.label('Switch mode:')\nui.button('Dark', on_click=dark.enable)\nui.button('Light', on_click=dark.disable)\n\nui.run()",
    "url": "/documentation/dark_mode#dark_mode"
  },
  {
    "title": "ui.dark_mode: Binding to a switch",
    "content": "The value of the `ui.dark_mode` element can be bound to other elements like a `ui.switch`.",
    "format": "md",
    "demo": "from nicegui import ui\n\ndark = ui.dark_mode()\nui.switch('Dark mode').bind_value(dark)\n\nui.run()",
    "url": "/documentation/dark_mode#binding_to_a_switch"
  },
  {
    "title": "ui.dark_mode: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/dark_mode#reference"
  },
  {
    "title": "ElementFilter: ElementFilter",
    "content": "Sometimes it is handy to search the Python element tree of the current page.\n``ElementFilter()`` allows powerful filtering by kind of elements, markers and content.\nIt also provides a fluent interface to apply more filters like excluding elements or filtering for elements within a specific parent.\nThe filter can be used as an iterator to iterate over the found elements and is always applied while iterating and not when being instantiated.\n\nAnd element is yielded if it matches all of the following conditions:\n\n- The element is of the specified kind (if specified).\n- The element is none of the excluded kinds.\n- The element has all of the specified markers.\n- The element has none of the excluded markers.\n- The element contains all of the specified content.\n- The element contains none of the excluded content.\n\n- Its ancestors include all of the specified instances defined via ``within``.\n- Its ancestors include none of the specified instances defined via ``not_within``.\n- Its ancestors include all of the specified kinds defined via ``within``.\n- Its ancestors include none of the specified kinds defined via ``not_within``.\n- Its ancestors include all of the specified markers defined via ``within``.\n- Its ancestors include none of the specified markers defined via ``not_within``.\n\nElement \"content\" includes its text, label, icon, placeholder, value, message, content, source.\nPartial matches like \"Hello\" in \"Hello World!\" are sufficient for content filtering.\n\n:param kind: filter by element type; the iterator will be of type ``kind``\n:param marker: filter by element markers; can be a list of strings or a single string where markers are separated by whitespace\n:param content: filter for elements which contain ``content`` in one of their content attributes like ``.text``, ``.value``, ``.source``, ...; can be a singe string or a list of strings which all must match\n:param local_scope: if `True`, only elements within the current scope are returned; by default the whole page is searched (this default behavior can be changed with ``ElementFilter.DEFAULT_LOCAL_SCOPE = True``)\n",
    "format": "rst",
    "demo": "from nicegui import ElementFilter, ui\n\nwith ui.card():\n    ui.button('button A')\n    ui.label('label A')\n\nwith ui.card().mark('important'):\n    ui.button('button B')\n    ui.label('label B')\n\nElementFilter(kind=ui.label).within(marker='important').classes('text-xl')\n\nui.run()",
    "url": "/documentation/element_filter#elementfilter"
  },
  {
    "title": "ElementFilter: Find all elements with text property",
    "content": "The `text` property is provided by a mixin called `TextElement`.\nIf we filter by such a mixin, the ElementFilter itself will provide a typed iterable.",
    "format": "md",
    "demo": "from nicegui import ElementFilter, ui\nfrom nicegui.elements.mixins.text_element import TextElement\n\nwith ui.card():\n    ui.button('button')\n    ui.icon('home')\n    ui.label('label A')\n    ui.label('label B')\n    ui.html('HTML')\n\nui.label(', '.join(b.text for b in ElementFilter(kind=TextElement)))\n\nui.run()",
    "url": "/documentation/element_filter#find_all_elements_with_text_property"
  },
  {
    "title": "ElementFilter: Markers",
    "content": "Markers are a simple way to tag elements with a string which can be queried by an `ElementFilter`.",
    "format": "md",
    "demo": "from nicegui import ElementFilter, ui\n\nwith ui.card().mark('red'):\n    ui.label('label A')\nwith ui.card().mark('strong'):\n    ui.label('label B')\nwith ui.card().mark('red strong'):\n    ui.label('label C')\n\nElementFilter(marker='red').classes('bg-red-200')\nElementFilter(marker='strong').classes('text-bold')\nElementFilter(marker='red strong').classes('bg-red-600 text-white')\n\nui.run()",
    "url": "/documentation/element_filter#markers"
  },
  {
    "title": "ElementFilter: Find elements on other pages",
    "content": "You can use the `app.clients` iterator to apply the element filter to all clients of a specific page.",
    "format": "md",
    "demo": "import time\nfrom nicegui import app, ui\n\n@ui.page('/log')\ndef page():\n    ui.log()\n\ndef log_time():\n    for client in app.clients('/log'):\n        with client:\n            for log in ElementFilter(kind=ui.log):\n                log.push(f'{time.strftime(\"%H:%M:%S\")}')\n\nui.button('Log current time', on_click=log_time)\nui.link('Open log', '/log', new_tab=True)\n\nui.run()",
    "url": "/documentation/element_filter#find_elements_on_other_pages"
  },
  {
    "title": "ElementFilter: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/element_filter#reference"
  },
  {
    "title": "ui.query: Query Selector",
    "content": "To manipulate elements like the document body, you can use the `ui.query` function.\nWith the query result you can add classes, styles, and attributes like with every other UI element.\nThis can be useful for example to change the background color of the page (e.g. `ui.query('body').classes('bg-green')`).\n\n:param selector: the CSS selector (e.g. \"body\", \"#my-id\", \".my-class\", \"div \u003E p\")\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\ndef set_background(color: str) -\u003E None:\n    ui.query('body').style(f'background-color: {color}')\n\nui.button('Blue', on_click=lambda: set_background('#ddeeff'))\nui.button('Orange', on_click=lambda: set_background('#ffeedd'))\n\nui.run()",
    "url": "/documentation/query#query_selector"
  },
  {
    "title": "ui.query: Set background gradient",
    "content": "It's easy to set a background gradient, image or similar.\nSee [w3schools.com](https://www.w3schools.com/cssref/pr_background-image.php) for more information about setting background with CSS.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.query('body').classes('bg-gradient-to-t from-blue-400 to-blue-100')\n\nui.run()",
    "url": "/documentation/query#set_background_gradient"
  },
  {
    "title": "ui.query: Modify default page padding",
    "content": "By default, NiceGUI provides a built-in padding around the content of the page.\nYou can modify it using the class selector `.nicegui-content`.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.query('.nicegui-content').classes('p-0')\nwith ui.column().classes('h-screen w-full bg-gray-400 justify-between'):\n    ui.label('top left')\n    ui.label('bottom right').classes('self-end')\n\nui.run()",
    "url": "/documentation/query#modify_default_page_padding"
  },
  {
    "title": "ui.query: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/query#reference"
  },
  {
    "title": "Styling & Appearance: Styling",
    "content": "NiceGUI uses the [Quasar Framework](https://quasar.dev/) and hence has its full design power.\nEach NiceGUI element provides a `props` method whose content is passed [to the Quasar component](https://justpy.io/quasar_tutorial/introduction/#props-of-quasar-components):\nHave a look at [the Quasar documentation](https://quasar.dev/vue-components/button#design) for all styling props.\nProps with a leading `:` can contain JavaScript expressions that are evaluated on the client.\nYou can also apply [Tailwind CSS](https://v3.tailwindcss.com/) utility classes with the `classes` method.\n\nIf you really need to apply CSS, you can use the `style` method. Here the delimiter is `;` instead of a blank space.\n\nAll three functions also provide `remove` and `replace` parameters in case the predefined look is not wanted in a particular styling.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.radio(['x', 'y', 'z'], value='x').props('inline color=green')\nui.button(icon='touch_app').props('outline round').classes('shadow-lg')\nui.label('Stylish!').style('color: #6E93D6; font-size: 200%; font-weight: 300')\n\nui.run()",
    "url": "/documentation/section_styling_appearance#styling"
  },
  {
    "title": "Styling & Appearance: Try styling NiceGUI elements!",
    "content": "\n    Try out how\n    [Tailwind CSS classes](https://v3.tailwindcss.com/),\n    [Quasar props](https://justpy.io/quasar_tutorial/introduction/#props-of-quasar-components),\n    and CSS styles affect NiceGUI elements.\n",
    "format": "md",
    "demo": "",
    "url": "/documentation/section_styling_appearance#try_styling_nicegui_elements_"
  },
  {
    "title": "Styling & Appearance: None",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/section_styling_appearance#None"
  },
  {
    "title": "Styling & Appearance: Tailwind CSS",
    "content": "[Tailwind CSS](https://v3.tailwindcss.com/) is a CSS framework for rapidly building custom user interfaces.\nNiceGUI provides a fluent, auto-complete friendly interface for adding Tailwind classes to UI elements.\n\nYou can discover available classes by navigating the methods of the `tailwind` property.\nThe builder pattern allows you to chain multiple classes together (as shown with \"Label A\").\nYou can also call the `tailwind` property with a list of classes (as shown with \"Label B\").\n\nAlthough this is very similar to using the `classes` method, it is more convenient for Tailwind classes due to auto-completion.\n\nLast but not least, you can also predefine a style and apply it to multiple elements (labels C and D).\n\nNote that sometimes Tailwind is overruled by Quasar styles, e.g. when using `ui.button('Button').tailwind('bg-red-500')`.\nThis is a known limitation and not fully in our control.\nBut we try to provide solutions like the `color` parameter: `ui.button('Button', color='red-500')`.",
    "format": "md",
    "demo": "from nicegui import Tailwind, ui\n\nui.label('Label A').tailwind.font_weight('extrabold').text_color('blue-600').background_color('orange-200')\nui.label('Label B').tailwind('drop-shadow', 'font-bold', 'text-green-600')\n\nred_style = Tailwind().text_color('red-600').font_weight('bold')\nlabel_c = ui.label('Label C')\nred_style.apply(label_c)\nui.label('Label D').tailwind(red_style)\n\nui.run()",
    "url": "/documentation/section_styling_appearance#tailwind_css"
  },
  {
    "title": "Styling & Appearance: Tailwind CSS Layers",
    "content": "Tailwind CSS' `@layer` directive allows you to define custom classes that can be used in your HTML.\nNiceGUI supports this feature by allowing you to add custom classes to the `components` layer.\nThis way, you can define your own classes and use them in your UI elements.\nIn the example below, we define a custom class `blue-box` and apply it to two labels.\nNote that the style tag is of type `text/tailwindcss` and not `text/css`.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.add_head_html('''\n    \u003Cstyle type=\"text/tailwindcss\"\u003E\n        @layer components {\n            .blue-box {\n                @apply bg-blue-500 p-12 text-center shadow-lg rounded-lg text-white;\n            }\n        }\n    \u003C/style\u003E\n''')\n\nwith ui.row():\n    ui.label('Hello').classes('blue-box')\n    ui.label('world').classes('blue-box')\n\nui.run()",
    "url": "/documentation/section_styling_appearance#tailwind_css_layers"
  },
  {
    "title": "Styling & Appearance: ElementFilter",
    "content": "Sometimes it is handy to search the Python element tree of the current page.\n``ElementFilter()`` allows powerful filtering by kind of elements, markers and content.\nIt also provides a fluent interface to apply more filters like excluding elements or filtering for elements within a specific parent.\nThe filter can be used as an iterator to iterate over the found elements and is always applied while iterating and not when being instantiated.\n\nAnd element is yielded if it matches all of the following conditions:\n\n- The element is of the specified kind (if specified).\n- The element is none of the excluded kinds.\n- The element has all of the specified markers.\n- The element has none of the excluded markers.\n- The element contains all of the specified content.\n- The element contains none of the excluded content.\n\n- Its ancestors include all of the specified instances defined via ``within``.\n- Its ancestors include none of the specified instances defined via ``not_within``.\n- Its ancestors include all of the specified kinds defined via ``within``.\n- Its ancestors include none of the specified kinds defined via ``not_within``.\n- Its ancestors include all of the specified markers defined via ``within``.\n- Its ancestors include none of the specified markers defined via ``not_within``.\n\nElement \"content\" includes its text, label, icon, placeholder, value, message, content, source.\nPartial matches like \"Hello\" in \"Hello World!\" are sufficient for content filtering.\n\n:param kind: filter by element type; the iterator will be of type ``kind``\n:param marker: filter by element markers; can be a list of strings or a single string where markers are separated by whitespace\n:param content: filter for elements which contain ``content`` in one of their content attributes like ``.text``, ``.value``, ``.source``, ...; can be a singe string or a list of strings which all must match\n:param local_scope: if `True`, only elements within the current scope are returned; by default the whole page is searched (this default behavior can be changed with ``ElementFilter.DEFAULT_LOCAL_SCOPE = True``)\n",
    "format": "rst",
    "demo": "from nicegui import ElementFilter, ui\n\nwith ui.card():\n    ui.button('button A')\n    ui.label('label A')\n\nwith ui.card().mark('important'):\n    ui.button('button B')\n    ui.label('label B')\n\nElementFilter(kind=ui.label).within(marker='important').classes('text-xl')\n\nui.run()",
    "url": "/documentation/section_styling_appearance#elementfilter"
  },
  {
    "title": "Styling & Appearance: Query Selector",
    "content": "To manipulate elements like the document body, you can use the `ui.query` function.\nWith the query result you can add classes, styles, and attributes like with every other UI element.\nThis can be useful for example to change the background color of the page (e.g. `ui.query('body').classes('bg-green')`).\n\n:param selector: the CSS selector (e.g. \"body\", \"#my-id\", \".my-class\", \"div \u003E p\")\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\ndef set_background(color: str) -\u003E None:\n    ui.query('body').style(f'background-color: {color}')\n\nui.button('Blue', on_click=lambda: set_background('#ddeeff'))\nui.button('Orange', on_click=lambda: set_background('#ffeedd'))\n\nui.run()",
    "url": "/documentation/section_styling_appearance#query_selector"
  },
  {
    "title": "Styling & Appearance: Color Theming",
    "content": "Sets the main colors (primary, secondary, accent, ...) used by `Quasar \u003Chttps://quasar.dev/style/theme-builder\u003E`_.\n\n:param primary: Primary color (default: \"#5898d4\")\n:param secondary: Secondary color (default: \"#26a69a\")\n:param accent: Accent color (default: \"#9c27b0\")\n:param dark: Dark color (default: \"#1d1d1d\")\n:param dark_page: Dark page color (default: \"#121212\")\n:param positive: Positive color (default: \"#21ba45\")\n:param negative: Negative color (default: \"#c10015\")\n:param info: Info color (default: \"#31ccec\")\n:param warning: Warning color (default: \"#f2c037\")\n:param custom_colors: Custom color definitions for branding (needs ``ui.colors`` to be called before custom color is ever used, *added in version 2.2.0*)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.button('Default', on_click=lambda: ui.colors())\nui.button('Gray', on_click=lambda: ui.colors(primary='#555'))\n\nui.run()",
    "url": "/documentation/section_styling_appearance#color_theming"
  },
  {
    "title": "Styling & Appearance: CSS Variables",
    "content": "You can customize the appearance of NiceGUI by setting CSS variables.\nCurrently, the following variables with their default values are available:\n\n- `--nicegui-default-padding: 1rem`\n- `--nicegui-default-gap: 1rem`\n",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.add_css('''\n    :root {\n        --nicegui-default-padding: 0.5rem;\n        --nicegui-default-gap: 3rem;\n    }\n''')\nwith ui.card():\n    ui.label('small padding')\n    ui.label('large gap')\n\nui.run()",
    "url": "/documentation/section_styling_appearance#css_variables"
  },
  {
    "title": "Styling & Appearance: Overwrite Tailwind's Default Style",
    "content": "Tailwind resets the default style of HTML elements, like the font size of `h2` elements in this example.\nYou can overwrite these defaults by adding a style tag with type `text/tailwindcss`.\nWithout this type, the style will be evaluated too early and will be overwritten by Tailwind.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.add_head_html('''\n    \u003Cstyle type=\"text/tailwindcss\"\u003E\n        h2 {\n            font-size: 150%;\n        }\n    \u003C/style\u003E\n''')\nui.html('\u003Ch2\u003EHello world!\u003C/h2\u003E')\n\nui.run()",
    "url": "/documentation/section_styling_appearance#overwrite_tailwind_s_default_style"
  },
  {
    "title": "Styling & Appearance: Dark mode",
    "content": "You can use this element to enable, disable or toggle dark mode on the page.\nThe value `None` represents auto mode, which uses the client's system preference.\n\nNote that this element overrides the `dark` parameter of the `ui.run` function and page decorators.\n\n:param value: Whether dark mode is enabled. If None, dark mode is set to auto.\n:param on_change: Callback that is invoked when the value changes.\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\ndark = ui.dark_mode()\nui.label('Switch mode:')\nui.button('Dark', on_click=dark.enable)\nui.button('Light', on_click=dark.disable)\n\nui.run()",
    "url": "/documentation/section_styling_appearance#dark_mode"
  },
  {
    "title": "Styling & Appearance: Add CSS style definitions to the page",
    "content": "This function can be used to add CSS style definitions to the head of the HTML page.\n\n*Added in version 2.0.0*\n\n:param content: CSS content (string or file path)\n:param shared: whether to add the code to all pages (default: ``False``, *added in version 2.14.0*)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.add_css('''\n    .red {\n        color: red;\n    }\n''')\nui.label('This is red with CSS.').classes('red')\n\nui.run()",
    "url": "/documentation/section_styling_appearance#add_css_style_definitions_to_the_page"
  },
  {
    "title": "Styling & Appearance: Using other Vue UI frameworks",
    "content": "**This is an experimental feature.**\n**Many NiceGUI elements are likely to break, and the API is subject to change.**\n\nNiceGUI uses the [Quasar Framework](https://quasar.dev/) by default.\nHowever, you can also try to use other Vue UI frameworks\nlike [Element Plus](https://element-plus.org/en-US/) or [Vuetify](https://vuetifyjs.com/en/).\nTo do so, you need to add the framework's JavaScript and CSS file to the head of your HTML document\nand configure NiceGUI accordingly by extending or replacing `app.config.vue_config_script`.\n\n*Added in NiceGUI 2.21.0*",
    "format": "md",
    "demo": "from nicegui import app, ui\n\nui.add_body_html('''\n    \u003Clink rel=\"stylesheet\" href=\"//unpkg.com/element-plus/dist/index.css\" /\u003E\n    \u003Cscript defer src=\"https://unpkg.com/element-plus\"\u003E\u003C/script\u003E\n''')\napp.config.vue_config_script += '''\n    app.use(ElementPlus);\n'''\n\nwith ui.element('el-button').on('click', lambda: ui.notify('Hi!')):\n    ui.html('Element Plus button')\n\nui.button('Quasar button', on_click=lambda: ui.notify('Ho!'))\n\nui.run()",
    "url": "/documentation/section_styling_appearance#using_other_vue_ui_frameworks"
  },
  {
    "title": "Project Structure: Project Structure",
    "content": "\n    The NiceGUI package provides a [pytest plugin](https://docs.pytest.org/en/stable/how-to/writing_plugins.html)\n    which can be activated via `pytest_plugins = ['nicegui.testing.plugin']`.\n    This makes specialized [fixtures](https://docs.pytest.org/en/stable/explanation/fixtures.html) available for testing your NiceGUI user interface.\n    With the [`screen` fixture](/documentation/screen) you can run the tests through a headless browser (slow)\n    and with the [`user` fixture](/documentation/user) fully simulated in Python (fast).\n    If you only want one kind of test fixtures,\n    you can also use the plugin `nicegui.testing.user_plugin` or `nicegui.testing.screen_plugin`.\n\n    There are a multitude of ways to structure your project and tests.\n    Here we only present two approaches which we found useful,\n    one for [small apps and experiments](/documentation/project_structure#simple)\n    and a [modular one for larger projects](/documentation/project_structure#modular).\n    You can find more information in the [pytest documentation](https://docs.pytest.org/en/stable/contents.html).\n",
    "format": "md",
    "demo": "",
    "url": "/documentation/project_structure#project_structure"
  },
  {
    "title": "Project Structure: Simple",
    "content": "\n    For small apps and experiments you can put the tests in a separate file,\n    as we do in the examples\n    [Chat App](https://github.com/zauberzeug/nicegui/tree/main/examples/chat_app)\n    [Todo List](https://github.com/zauberzeug/nicegui/tree/main/examples/todo_list/) and\n    [Authentication](https://github.com/zauberzeug/nicegui/tree/main/examples/authentication).\n    To properly re-initialize your `main.py` in the tests,\n    you place an empty `__init__.py` file next to your code to make it a package\n    and use the `module_under_test` marker to automatically reload your main file for each test.\n    Also don't forget the `pytest.ini` file\n    to enable the [`asyncio_mode = auto`](/documentation/user#async_execution) option for the user fixture\n    and make sure you properly guard the `ui.run()` call in your `main.py`\n    to prevent the server from starting during the tests:\n",
    "format": "md",
    "demo": "",
    "url": "/documentation/project_structure#simple"
  },
  {
    "title": "Project Structure: None",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/project_structure#None"
  },
  {
    "title": "Project Structure: None",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/project_structure#None"
  },
  {
    "title": "Project Structure: Modular",
    "content": "\n    A more modular approach is to create a package for your code with an empty `__init__.py`\n    and a separate `tests` folder for your tests.\n    In your package a `startup.py` file can be used to register pages and do all necessary app initialization.\n    The `main.py` at root level then only imports the startup routine and calls `ui.run()`.\n    An empty `conftest.py` file in the root directory makes the package with its `startup` routine available to the tests.\n    Also don't forget the `pytest.ini` file\n    to enable the [`asyncio_mode = auto`](/documentation/user#async_execution) option for the user fixture.\n",
    "format": "md",
    "demo": "",
    "url": "/documentation/project_structure#modular"
  },
  {
    "title": "Project Structure: None",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/project_structure#None"
  },
  {
    "title": "Project Structure: ",
    "content": "\n    You can also define your own fixtures in the `conftest.py` which call the `startup` routine.\n    Pytest has some magic to automatically find and use this specialized fixture in your tests.\n    This way you can keep your tests clean and simple.\n    See the [pytests example](https://github.com/zauberzeug/nicegui/tree/main/examples/pytests)\n    for a full demonstration of this setup.\n",
    "format": "md",
    "demo": "",
    "url": "/documentation/project_structure#None"
  },
  {
    "title": "Project Structure: None",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/project_structure#None"
  },
  {
    "title": "Screen Fixture: Screen Fixture",
    "content": "\n        The `screen` fixture starts a real (headless) browser to interact with your application.\n        This is only necessary if you have browser-specific behavior to test.\n        NiceGUI itself is thoroughly tested with this fixture to ensure each component works as expected.\n        So only use it if you have to.\n    ",
    "format": "md",
    "demo": "",
    "url": "/documentation/screen#screen_fixture"
  },
  {
    "title": "Screen Fixture: Web driver",
    "content": "\n        The `screen` fixture uses Selenium under the hood.\n        Currently it is only tested with the Chrome driver.\n        To automatically use it for the tests we suggest to add the option `--driver Chrome` to your `pytest.ini`:\n    ",
    "format": "md",
    "demo": "",
    "url": "/documentation/screen#web_driver"
  },
  {
    "title": "Screen Fixture: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/screen#reference"
  },
  {
    "title": "User Fixture: User Fixture",
    "content": "\n        We recommend utilizing the `user` fixture instead of the [`screen` fixture](/documentation/screen) wherever possible\n        because execution is as fast as unit tests and it does not need Selenium as a dependency\n        when loaded via `pytest_plugins = ['nicegui.testing.user_plugin']`.\n        The `user` fixture cuts away the browser and replaces it by a lightweight simulation entirely in Python.\n        See [project structure](/documentation/project_structure) for a description of the setup.\n\n        You can assert to \"see\" specific elements or content, click buttons, type into inputs and trigger events.\n        We aimed for a nice API to write acceptance tests which read like a story and are easy to understand.\n        Due to the fast execution, the classical [test pyramid](https://martinfowler.com/bliki/TestPyramid.html),\n        where UI tests are considered slow and expensive, does not apply anymore.\n    \n        **NOTE:** The `user` fixture is quite new and still misses some features.\n        Please let us know in separate feature requests\n        [over on GitHub](https://github.com/zauberzeug/nicegui/discussions/new?category=ideas-feature-requests).\n    ",
    "format": "md",
    "demo": "",
    "url": "/documentation/user#user_fixture"
  },
  {
    "title": "User Fixture: Async execution",
    "content": "\n        The user simulation runs in the same async context as your app\n        to make querying and interaction as easy as possible.\n        But that also means that your tests must be `async`.\n        We suggest to activate the [pytest-asyncio auto-mode](https://pytest-asyncio.readthedocs.io/en/latest/concepts.html#auto-mode)\n        by either creating a `pytest.ini` file in your project root\n        or adding the activation directly to your `pyproject.toml`.\n    ",
    "format": "md",
    "demo": "",
    "url": "/documentation/user#async_execution"
  },
  {
    "title": "User Fixture: Querying",
    "content": "\n    The querying capabilities of the `User` are built upon the [ElementFilter](/documentation/element_filter).\n    The `user.should_see(...)` method and `user.find(...)` method\n    provide parameters to filter for content, [markers](/documentation/element_filter#markers), types, etc.\n    If you do not provide a named property, the string will match against the text content and markers.\n",
    "format": "md",
    "demo": "",
    "url": "/documentation/user#querying"
  },
  {
    "title": "User Fixture: None",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/user#None"
  },
  {
    "title": "User Fixture: User Interaction",
    "content": "\n    `user.find(...)` returns a `UserInteraction` object which provides methods to type text,\n    clear inputs, click buttons and trigger events on the found elements.\n    This demo shows how to trigger a \"keydown.tab\" event to autocomplete an input field after typing the first letter.\n\n    *Added in version 2.7.0: triggering events*\n",
    "format": "md",
    "demo": "",
    "url": "/documentation/user#user_interaction"
  },
  {
    "title": "User Fixture: None",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/user#None"
  },
  {
    "title": "User Fixture: Selecting options",
    "content": "\n    To choose items in a `ui.select` simply\n\n    - locate the `ui.select` element using `user.find()`,\n    - use `click()` to open the dropdown,\n    - locate the specific _option_ you want to select, again using `user.find()`, and\n    - use `click()` a second time to select the desired option.\n\n    For a multi-select element, repeat the click-and-choose steps for each item.\n",
    "format": "md",
    "demo": "",
    "url": "/documentation/user#selecting_options"
  },
  {
    "title": "User Fixture: None",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/user#None"
  },
  {
    "title": "User Fixture: Using an ElementFilter",
    "content": "\n    It may be desirable to use an [`ElementFilter`](/documentation/element_filter) to\n\n    - preserve the order of elements to check their order on the page, and\n    - more granular filtering options, such as `ElementFilter(...).within(...)`.\n\n    By entering the `user` context and iterating over `ElementFilter`,\n    you can preserve the natural document order of matching elements:\n",
    "format": "md",
    "demo": "",
    "url": "/documentation/user#using_an_elementfilter"
  },
  {
    "title": "User Fixture: None",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/user#None"
  },
  {
    "title": "User Fixture: Complex elements",
    "content": "\n    There are some elements with complex visualization and interaction behaviors (`ui.upload`, `ui.table`, ...).\n    Not every aspect of these elements can be tested with `should_see` and `UserInteraction`.\n    Still, you can grab them with `user.find(...)` and do the testing on the elements themselves.\n",
    "format": "md",
    "demo": "",
    "url": "/documentation/user#complex_elements"
  },
  {
    "title": "User Fixture: None",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/user#None"
  },
  {
    "title": "User Fixture: Test Downloads",
    "content": "\n    You can verify that a download was triggered by checking `user.downloads.http_responses`.\n    By awaiting `user.downloads.next()` you can get the next download response.\n\n    *Added in version 2.1.0*\n",
    "format": "md",
    "demo": "",
    "url": "/documentation/user#test_downloads"
  },
  {
    "title": "User Fixture: None",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/user#None"
  },
  {
    "title": "User Fixture: Multiple Users",
    "content": "\n    Sometimes it is not enough to just interact with the UI as a single user.\n    Besides the `user` fixture, we also provide the `create_user` fixture which is a factory function to create users.\n    The `User` instances are independent from each other and can interact with the UI in parallel.\n    See our [Chat App example](https://github.com/zauberzeug/nicegui/blob/main/examples/chat_app/test_chat_app.py)\n    for a full demonstration.\n",
    "format": "md",
    "demo": "",
    "url": "/documentation/user#multiple_users"
  },
  {
    "title": "User Fixture: None",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/user#None"
  },
  {
    "title": "User Fixture: Simulate JavasScript",
    "content": "\n    The `User` class has a `javascript_rules` dictionary to simulate JavaScript execution.\n    The key is a compiled regular expression and the value is a function that returns the JavaScript response.\n    The function will be called with the match object of the regular expression on the JavaScript command.\n\n    *Added in version 2.14.0*\n",
    "format": "md",
    "demo": "",
    "url": "/documentation/user#simulate_javasscript"
  },
  {
    "title": "User Fixture: None",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/user#None"
  },
  {
    "title": "User Fixture: Comparison with the screen fixture",
    "content": "\n    By cutting out the browser, test execution becomes much faster than the [`screen` fixture](/documentation/screen).\n    See our [pytests example](https://github.com/zauberzeug/nicegui/tree/main/examples/pytests)\n    which implements the same tests with both fixtures.\n    Of course, some features like screenshots or browser-specific behavior are not available,\n    but in most cases the speed of the `user` fixture makes it the first choice.\n",
    "format": "md",
    "demo": "",
    "url": "/documentation/user#comparison_with_the_screen_fixture"
  },
  {
    "title": "User Fixture: User Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/user#user_reference"
  },
  {
    "title": "User Fixture: UserInteraction Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/user#userinteraction_reference"
  },
  {
    "title": "Testing: Project Structure",
    "content": "\n    The NiceGUI package provides a [pytest plugin](https://docs.pytest.org/en/stable/how-to/writing_plugins.html)\n    which can be activated via `pytest_plugins = ['nicegui.testing.plugin']`.\n    This makes specialized [fixtures](https://docs.pytest.org/en/stable/explanation/fixtures.html) available for testing your NiceGUI user interface.\n    With the [`screen` fixture](/documentation/screen) you can run the tests through a headless browser (slow)\n    and with the [`user` fixture](/documentation/user) fully simulated in Python (fast).\n    If you only want one kind of test fixtures,\n    you can also use the plugin `nicegui.testing.user_plugin` or `nicegui.testing.screen_plugin`.\n\n    There are a multitude of ways to structure your project and tests.\n    Here we only present two approaches which we found useful,\n    one for [small apps and experiments](/documentation/project_structure#simple)\n    and a [modular one for larger projects](/documentation/project_structure#modular).\n    You can find more information in the [pytest documentation](https://docs.pytest.org/en/stable/contents.html).\n",
    "format": "md",
    "demo": "",
    "url": "/documentation/section_testing#project_structure"
  },
  {
    "title": "Testing: User Fixture",
    "content": "\n        We recommend utilizing the `user` fixture instead of the [`screen` fixture](/documentation/screen) wherever possible\n        because execution is as fast as unit tests and it does not need Selenium as a dependency\n        when loaded via `pytest_plugins = ['nicegui.testing.user_plugin']`.\n        The `user` fixture cuts away the browser and replaces it by a lightweight simulation entirely in Python.\n        See [project structure](/documentation/project_structure) for a description of the setup.\n\n        You can assert to \"see\" specific elements or content, click buttons, type into inputs and trigger events.\n        We aimed for a nice API to write acceptance tests which read like a story and are easy to understand.\n        Due to the fast execution, the classical [test pyramid](https://martinfowler.com/bliki/TestPyramid.html),\n        where UI tests are considered slow and expensive, does not apply anymore.\n    \n        **NOTE:** The `user` fixture is quite new and still misses some features.\n        Please let us know in separate feature requests\n        [over on GitHub](https://github.com/zauberzeug/nicegui/discussions/new?category=ideas-feature-requests).\n    ",
    "format": "md",
    "demo": "",
    "url": "/documentation/section_testing#user_fixture"
  },
  {
    "title": "Testing: Screen Fixture",
    "content": "\n        The `screen` fixture starts a real (headless) browser to interact with your application.\n        This is only necessary if you have browser-specific behavior to test.\n        NiceGUI itself is thoroughly tested with this fixture to ensure each component works as expected.\n        So only use it if you have to.\n    ",
    "format": "md",
    "demo": "",
    "url": "/documentation/section_testing#screen_fixture"
  },
  {
    "title": "ui.chat_message: Chat Message",
    "content": "Based on Quasar's `Chat Message \u003Chttps://quasar.dev/vue-components/chat/\u003E`_ component.\n\n:param text: the message body (can be a list of strings for multiple message parts)\n:param name: the name of the message author\n:param label: renders a label header/section only\n:param stamp: timestamp of the message\n:param avatar: URL to an avatar\n:param sent: render as a sent message (so from current user) (default: False)\n:param text_html: render text as HTML (default: False)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.chat_message('Hello NiceGUI!',\n                name='Robot',\n                stamp='now',\n                avatar='https://robohash.org/ui')\n\nui.run()",
    "url": "/documentation/chat_message#chat_message"
  },
  {
    "title": "ui.chat_message: HTML text",
    "content": "Using the `text_html` parameter, you can send HTML text to the chat.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.chat_message('Without \u003Cstrong\u003EHTML\u003C/strong\u003E')\nui.chat_message('With \u003Cstrong\u003EHTML\u003C/strong\u003E', text_html=True)\n\nui.run()",
    "url": "/documentation/chat_message#html_text"
  },
  {
    "title": "ui.chat_message: Newline",
    "content": "You can use newlines in the chat message.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.chat_message('This is a\\nlong line!')\n\nui.run()",
    "url": "/documentation/chat_message#newline"
  },
  {
    "title": "ui.chat_message: Multi-part messages",
    "content": "You can send multiple message parts by passing a list of strings.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.chat_message(['Hi! 😀', 'How are you?']\n                )\n\nui.run()",
    "url": "/documentation/chat_message#multi-part_messages"
  },
  {
    "title": "ui.chat_message: Chat message with child elements",
    "content": "You can add child elements to a chat message.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.chat_message():\n    ui.label('Guess where I am!')\n    ui.image('https://picsum.photos/id/249/640/360').classes('w-64')\n\nui.run()",
    "url": "/documentation/chat_message#chat_message_with_child_elements"
  },
  {
    "title": "ui.chat_message: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/chat_message#reference"
  },
  {
    "title": "ui.element: Generic Element",
    "content": "This class is the base class for all other UI elements.\nBut you can use it to create elements with arbitrary HTML tags.\n\n:param tag: HTML tag of the element\n:param _client: client for this element (for internal use only)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.element('div').classes('p-2 bg-blue-100'):\n    ui.label('inside a colored div')\n\nui.run()",
    "url": "/documentation/element#generic_element"
  },
  {
    "title": "ui.element: Register event handlers",
    "content": "The event handler can be a Python function, a JavaScript function or a combination of both:\n\n- If you want to handle the event on the server with all (serializable) event arguments,\n    use a Python ``handler``.\n\n- If you want to handle the event on the client side without emitting anything to the server,\n    use ``js_handler`` with a JavaScript function handling the event.\n\n- If you want to handle the event on the server with a subset or transformed version of the event arguments,\n    use ``js_handler`` with a JavaScript function emitting the transformed arguments using ``emit()``, and\n    use a Python ``handler`` to handle these arguments on the server side.\n\n    The ``js_handler`` can also decide to selectively emit arguments to the server,\n    in which case the Python ``handler`` will not always be called.\n\n*Updated in version 2.18.0: Both handlers can be specified at the same time.*",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.button('Python handler') \\\n    .on('click',\n        lambda e: ui.notify(f'click: ({e.args[\"clientX\"]}, {e.args[\"clientY\"]})'))\n\nui.button('JavaScript handler') \\\n    .on('click',\n        js_handler='(e) =\u003E alert(`click: (${e.clientX}, ${e.clientY})`)')\n\nui.button('Combination') \\\n    .on('click',\n        lambda e: ui.notify(f'click: {e.args}'),\n        js_handler='(e) =\u003E emit(e.clientX, e.clientY)')\n\nui.run()",
    "url": "/documentation/element#register_event_handlers"
  },
  {
    "title": "ui.element: Move elements",
    "content": "This demo shows how to move elements between or within containers.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.card() as a:\n    ui.label('A')\n    x = ui.label('X')\n\nwith ui.card() as b:\n    ui.label('B')\n\nui.button('Move X to A', on_click=lambda: x.move(a))\nui.button('Move X to B', on_click=lambda: x.move(b))\nui.button('Move X to top', on_click=lambda: x.move(target_index=0))\n\nui.run()",
    "url": "/documentation/element#move_elements"
  },
  {
    "title": "ui.element: Move elements to slots",
    "content": "This demo shows how to move elements between slots within an element.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.card() as card:\n    name = ui.input('Name', value='Paul')\n    name.add_slot('append')\n    icon = ui.icon('face')\n\nui.button('Move into input', on_click=lambda: icon.move(name, target_slot='append'))\nui.button('Move out of input', on_click=lambda: icon.move(card))\n\nui.run()",
    "url": "/documentation/element#move_elements_to_slots"
  },
  {
    "title": "ui.element: Default props",
    "content": "You can set default props for all elements of a certain class.\nThis way you can avoid repeating the same props over and over again.\n\nDefault props only apply to elements created after the default props were set.\nSubclasses inherit the default props of their parent class.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.button.default_props('rounded outline')\nui.button('Button A')\nui.button('Button B')\n\nui.run()",
    "url": "/documentation/element#default_props"
  },
  {
    "title": "ui.element: Default classes",
    "content": "You can set default classes for all elements of a certain class.\nThis way you can avoid repeating the same classes over and over again.\n\nDefault classes only apply to elements created after the default classes were set.\nSubclasses inherit the default classes of their parent class.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.label.default_classes('bg-blue-100 p-2')\nui.label('Label A')\nui.label('Label B')\n\nui.run()",
    "url": "/documentation/element#default_classes"
  },
  {
    "title": "ui.element: Default style",
    "content": "You can set a default style for all elements of a certain class.\nThis way you can avoid repeating the same style over and over again.\n\nA default style only applies to elements created after the default style was set.\nSubclasses inherit the default style of their parent class.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.label.default_style('color: tomato')\nui.label('Label A')\nui.label('Label B')\n\nui.run()",
    "url": "/documentation/element#default_style"
  },
  {
    "title": "ui.element: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/element#reference"
  },
  {
    "title": "ui.html: HTML Element",
    "content": "Renders arbitrary HTML onto the page, wrapped in the specified tag.\n`Tailwind \u003Chttps://v3.tailwindcss.com/\u003E`_ can be used for styling.\nYou can also use `ui.add_head_html` to add html code into the head of the document and `ui.add_body_html`\nto add it into the body.\n\n:param content: the HTML code to be displayed\n:param tag: the HTML tag to wrap the content in (default: \"div\")\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.html('This is \u003Cstrong\u003EHTML\u003C/strong\u003E.')\n\nui.run()",
    "url": "/documentation/html#html_element"
  },
  {
    "title": "ui.html: Producing in-line elements",
    "content": "Use the `tag` parameter to produce something other than a div.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.html('This is \u003Cu\u003Eemphasized\u003C/u\u003E.', tag='em')\n\nui.run()",
    "url": "/documentation/html#producing_in-line_elements"
  },
  {
    "title": "ui.html: Other HTML Elements",
    "content": "There is also an `html` module that allows you to insert other HTML elements like `\u003Cspan\u003E`, `\u003Cdiv\u003E`, `\u003Cp\u003E`, etc.\nIt is equivalent to using the `ui.element` method with the `tag` argument.\n\nLike with any other element, you can add classes, style, props, tooltips and events.\nOne convenience is that the keyword arguments are automatically added to the element's `props` dictionary.\n\n*Added in version 2.5.0*",
    "format": "md",
    "demo": "from nicegui import html, ui\n\nwith html.section().style('font-size: 120%'):\n    html.strong('This is bold.') \\\n        .classes('cursor-pointer') \\\n        .on('click', lambda: ui.notify('Bold!'))\n    html.hr()\n    html.em('This is italic.').tooltip('Nice!')\n    with ui.row():\n        html.img().props('src=https://placehold.co/60')\n        html.img(src='https://placehold.co/60')\n\nui.run()",
    "url": "/documentation/html#other_html_elements"
  },
  {
    "title": "ui.html: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/html#reference"
  },
  {
    "title": "ui.label: Label",
    "content": "Displays some text.\n\n:param text: the content of the label\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.label('some label')\n\nui.run()",
    "url": "/documentation/label#label"
  },
  {
    "title": "ui.label: Change Appearance Depending on the Content",
    "content": "You can overwrite the `_handle_text_change` method to update other attributes of a label depending on its content.\nThis technique also works for bindings as shown in the example below.",
    "format": "md",
    "demo": "from nicegui import ui\n\nclass status_label(ui.label):\n    def _handle_text_change(self, text: str) -\u003E None:\n        super()._handle_text_change(text)\n        if text == 'ok':\n            self.classes(replace='text-positive')\n        else:\n            self.classes(replace='text-negative')\n\nmodel = {'status': 'error'}\nstatus_label().bind_text_from(model, 'status')\nui.switch(on_change=lambda e: model.update(status='ok' if e.value else 'error'))\n\nui.run()",
    "url": "/documentation/label#change_appearance_depending_on_the_content"
  },
  {
    "title": "ui.label: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/label#reference"
  },
  {
    "title": "ui.link: Link",
    "content": "Create a hyperlink.\n\nTo jump to a specific location within a page you can place linkable anchors with `ui.link_target(\"name\")`\nand link to it with `ui.link(target=\"#name\")`.\n\n:param text: display text\n:param target: page function, NiceGUI element on the same page or string that is a an absolute URL or relative path from base URL\n:param new_tab: open link in new tab (default: False)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.link('NiceGUI on GitHub', 'https://github.com/zauberzeug/nicegui')\n\nui.run()",
    "url": "/documentation/link#link"
  },
  {
    "title": "ui.link: Navigate on large pages",
    "content": "To jump to a specific location within a page you can place linkable anchors with `ui.link_target('target_name')`\nor simply pass a NiceGUI element as link target.",
    "format": "md",
    "demo": "from nicegui import ui\n\nnavigation = ui.row()\nui.link_target('target_A')\nui.label(\n    'Lorem ipsum dolor sit amet, consectetur adipiscing elit, '\n    'sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'\n)\nlabel_B = ui.label(\n    'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. '\n    'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. '\n    'Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'\n)\nwith navigation:\n    ui.link('Goto A', '#target_A')\n    ui.link('Goto B', label_B)\n\nui.run()",
    "url": "/documentation/link#navigate_on_large_pages"
  },
  {
    "title": "ui.link: Links to other pages",
    "content": "You can link to other pages by providing the link target as path or function reference.",
    "format": "md",
    "demo": "from nicegui import ui\n\n@ui.page('/some_other_page')\ndef my_page():\n    ui.label('This is another page')\n\nui.label('Go to other page')\nui.link('... with path', '/some_other_page')\nui.link('... with function reference', my_page)\n\nui.run()",
    "url": "/documentation/link#links_to_other_pages"
  },
  {
    "title": "ui.link: Link from images and other elements",
    "content": "By nesting elements inside a link you can make the whole element clickable.\nThis works with all elements but is most useful for non-interactive elements like\n[ui.image](/documentation/image), [ui.avatar](/documentation/image) etc.",
    "format": "md",
    "demo": "from nicegui import ui\n\nwith ui.link(target='https://github.com/zauberzeug/nicegui'):\n    ui.image('https://picsum.photos/id/41/640/360').classes('w-64')\n\nui.run()",
    "url": "/documentation/link#link_from_images_and_other_elements"
  },
  {
    "title": "ui.link: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/link#reference"
  },
  {
    "title": "ui.markdown: Markdown Element",
    "content": "Renders Markdown onto the page.\n\n:param content: the Markdown content to be displayed\n:param extras: list of `markdown2 extensions \u003Chttps://github.com/trentm/python-markdown2/wiki/Extras#implemented-extras\u003E`_ (default: `['fenced-code-blocks', 'tables']`)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.markdown('This is **Markdown**.')\n\nui.run()",
    "url": "/documentation/markdown#markdown_element"
  },
  {
    "title": "ui.markdown: Markdown with indentation",
    "content": "Common indentation is automatically stripped from the beginning of each line.\nSo you can indent markdown elements, and they will still be rendered correctly.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.markdown('''\n    ## Example\n\n    This line is not indented.\n\n        This block is indented.\n        Thus it is rendered as source code.\n\n    This is normal text again.\n''')\n\nui.run()",
    "url": "/documentation/markdown#markdown_with_indentation"
  },
  {
    "title": "ui.markdown: Markdown with code blocks",
    "content": "You can use code blocks to show code examples.\nIf you specify the language after the opening triple backticks, the code will be syntax highlighted.\nSee [the Pygments website](https://pygments.org/languages/) for a list of supported languages.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.markdown('''\n    ```python\n    from nicegui import ui\n\n    ui.label('Hello World!')\n\n    ui.run(dark=True)\n    ```\n''')\n\nui.run()",
    "url": "/documentation/markdown#markdown_with_code_blocks"
  },
  {
    "title": "ui.markdown: Markdown tables",
    "content": "By activating the \"tables\" extra, you can use Markdown tables.\nSee the [markdown2 documentation](https://github.com/trentm/python-markdown2/wiki/Extras#implemented-extras) for a list of available extras.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.markdown('''\n    | First name | Last name |\n    | ---------- | --------- |\n    | Max        | Planck    |\n    | Marie      | Curie     |\n''', extras=['tables'])\n\nui.run()",
    "url": "/documentation/markdown#markdown_tables"
  },
  {
    "title": "ui.markdown: Mermaid diagrams",
    "content": "You can use Mermaid diagrams with the \"mermaid\" extra.\nSee the [markdown2 documentation](https://github.com/trentm/python-markdown2/wiki/Extras#implemented-extras)\nfor a list of available extras.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.markdown('''\n    ```mermaid\n    graph TD;\n        A--\u003EB;\n        A--\u003EC;\n        B--\u003ED;\n        C--\u003ED;\n    ```\n''', extras=['mermaid'])\n\nui.run()",
    "url": "/documentation/markdown#mermaid_diagrams"
  },
  {
    "title": "ui.markdown: LaTeX formulas",
    "content": "By activating the \"latex\" extra, you can use LaTeX formulas.\nThis requires markdown2 version \u003E=2.5 as well as latex2mathml to be installed.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.markdown(r'''\n    Euler's identity:\n\n    $$e^{i\\pi} = -1$$\n''', extras=['latex'])\n\nui.run()",
    "url": "/documentation/markdown#latex_formulas"
  },
  {
    "title": "ui.markdown: Change Markdown content",
    "content": "You can change the content of a Markdown element by setting its `content` property or calling `set_content`.",
    "format": "md",
    "demo": "from nicegui import ui\n\nmarkdown = ui.markdown('Sample content')\nui.button('Change Content', on_click=lambda: markdown.set_content('This is new content'))\n\nui.run()",
    "url": "/documentation/markdown#change_markdown_content"
  },
  {
    "title": "ui.markdown: Styling elements inside Markdown",
    "content": "To style HTML elements inside a `ui.markdown` element, you can add custom CSS rules for the \"nicegui-markdown\" class.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.add_css('''\n    .nicegui-markdown a {\n        color: orange;\n        text-decoration: none;\n    }\n    .nicegui-markdown a:hover {\n        color: orange;\n        text-decoration: underline;\n    }\n''')\nui.markdown('This is a [link](https://example.com).')\n\nui.run()",
    "url": "/documentation/markdown#styling_elements_inside_markdown"
  },
  {
    "title": "ui.markdown: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/markdown#reference"
  },
  {
    "title": "ui.mermaid: Mermaid Diagrams",
    "content": "Renders diagrams and charts written in the Markdown-inspired `Mermaid \u003Chttps://mermaid.js.org/\u003E`_ language.\nThe mermaid syntax can also be used inside Markdown elements by providing the extension string 'mermaid' to the ``ui.markdown`` element.\n\nThe optional configuration dictionary is passed directly to mermaid before the first diagram is rendered.\nThis can be used to set such options as\n\n    ``{'securityLevel': 'loose', ...}`` - allow running JavaScript when a node is clicked\n    ``{'logLevel': 'info', ...}`` - log debug info to the console\n\nRefer to the Mermaid documentation for the ``mermaid.initialize()`` method for a full list of options.\n\n:param content: the Mermaid content to be displayed\n:param config: configuration dictionary to be passed to ``mermaid.initialize()``\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.mermaid('''\ngraph LR;\n    A --\u003E B;\n    A --\u003E C;\n''')\n\nui.run()",
    "url": "/documentation/mermaid#mermaid_diagrams"
  },
  {
    "title": "ui.mermaid: Handle click events",
    "content": "You can register to click events by adding a `click` directive to a node and emitting a custom event.\nMake sure to set the `securityLevel` to `loose` in the `config` parameter to allow JavaScript execution.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.mermaid('''\ngraph LR;\n    A((Click me!));\n    click A call emitEvent(\"mermaid_click\", \"You clicked me!\")\n''', config={'securityLevel': 'loose'})\nui.on('mermaid_click', lambda e: ui.notify(e.args))\n\nui.run()",
    "url": "/documentation/mermaid#handle_click_events"
  },
  {
    "title": "ui.mermaid: Handle errors",
    "content": "You can handle errors by listening to the `error` event.\nThe event `args` contain the properties `hash`, `message`, `str` and an `error` object with additional information.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.mermaid('''\ngraph LR;\n    A --\u003E B;\n    A -\u003E C;\n''').on('error', lambda e: print(e.args['message']))\n\nui.run()",
    "url": "/documentation/mermaid#handle_errors"
  },
  {
    "title": "ui.mermaid: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/mermaid#reference"
  },
  {
    "title": "ui.restructured_text: ReStructuredText",
    "content": "Renders ReStructuredText onto the page.\n\n:param content: the ReStructuredText content to be displayed\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.restructured_text('This is **reStructuredText**.')\n\nui.run()",
    "url": "/documentation/restructured_text#restructuredtext"
  },
  {
    "title": "ui.restructured_text: reStructuredText with indentation",
    "content": "You can indent reStructuredText elements to create a hierarchy.\nCommon indentation is automatically stripped from the beginning of each line to preserve the relative indentation,\nso you can indent multiline strings.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.restructured_text('''\n    This is an example of a reStructuredText paragraph with several indentation levels.\n\n    You can use multiple levels of indentation to structure your content.\n    Each level of indentation represents a different level of hierarchy.\n\n    - Level 1\n        - Level 2\n            - Level 3\n                - Level 4\n                    - Level 5\n''')\n\nui.run()",
    "url": "/documentation/restructured_text#restructuredtext_with_indentation"
  },
  {
    "title": "ui.restructured_text: reStructuredText with code blocks",
    "content": "You can use code blocks to show code examples.\nIf you specify the language, the code will be syntax-highlighted.\nSee [this link](https://docs.typo3.org/m/typo3/docs-how-to-document/main/en-us/WritingReST/Reference/Code/Codeblocks.html#writing-rest-codeblocks-available-lexers) for a list of supported languages.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.restructured_text('''\n    .. code-block:: python3\n\n        from nicegui import ui\n\n        ui.label('Hello World!')\n\n        ui.run()\n''')\n\nui.run()",
    "url": "/documentation/restructured_text#restructuredtext_with_code_blocks"
  },
  {
    "title": "ui.restructured_text: reStructuredText with tables",
    "content": "See the [sphinx documentation](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#tables)\nfor more information about reStructuredText tables.",
    "format": "md",
    "demo": "from nicegui import ui\n\nui.restructured_text('''\n    +-------+-------+---------+--------+\n    | A     | B     | A and B | A or B |\n    +=======+=======+=========+========+\n    | False | False | False   | False  |\n    +-------+-------+---------+--------+\n    | True  | False | False   | True   |\n    +-------+-------+---------+--------+\n    | False | True  | False   | True   |\n    +-------+-------+---------+--------+\n    | True  | True  | True    | True   |\n    +-------+-------+---------+--------+\n''')\n\nui.run()",
    "url": "/documentation/restructured_text#restructuredtext_with_tables"
  },
  {
    "title": "ui.restructured_text: Reference",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/restructured_text#reference"
  },
  {
    "title": "Text Elements: Label",
    "content": "Displays some text.\n\n:param text: the content of the label\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.label('some label')\n\nui.run()",
    "url": "/documentation/section_text_elements#label"
  },
  {
    "title": "Text Elements: Link",
    "content": "Create a hyperlink.\n\nTo jump to a specific location within a page you can place linkable anchors with `ui.link_target(\"name\")`\nand link to it with `ui.link(target=\"#name\")`.\n\n:param text: display text\n:param target: page function, NiceGUI element on the same page or string that is a an absolute URL or relative path from base URL\n:param new_tab: open link in new tab (default: False)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.link('NiceGUI on GitHub', 'https://github.com/zauberzeug/nicegui')\n\nui.run()",
    "url": "/documentation/section_text_elements#link"
  },
  {
    "title": "Text Elements: Chat Message",
    "content": "Based on Quasar's `Chat Message \u003Chttps://quasar.dev/vue-components/chat/\u003E`_ component.\n\n:param text: the message body (can be a list of strings for multiple message parts)\n:param name: the name of the message author\n:param label: renders a label header/section only\n:param stamp: timestamp of the message\n:param avatar: URL to an avatar\n:param sent: render as a sent message (so from current user) (default: False)\n:param text_html: render text as HTML (default: False)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.chat_message('Hello NiceGUI!',\n                name='Robot',\n                stamp='now',\n                avatar='https://robohash.org/ui')\n\nui.run()",
    "url": "/documentation/section_text_elements#chat_message"
  },
  {
    "title": "Text Elements: Generic Element",
    "content": "This class is the base class for all other UI elements.\nBut you can use it to create elements with arbitrary HTML tags.\n\n:param tag: HTML tag of the element\n:param _client: client for this element (for internal use only)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nwith ui.element('div').classes('p-2 bg-blue-100'):\n    ui.label('inside a colored div')\n\nui.run()",
    "url": "/documentation/section_text_elements#generic_element"
  },
  {
    "title": "Text Elements: Markdown Element",
    "content": "Renders Markdown onto the page.\n\n:param content: the Markdown content to be displayed\n:param extras: list of `markdown2 extensions \u003Chttps://github.com/trentm/python-markdown2/wiki/Extras#implemented-extras\u003E`_ (default: `['fenced-code-blocks', 'tables']`)\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.markdown('This is **Markdown**.')\n\nui.run()",
    "url": "/documentation/section_text_elements#markdown_element"
  },
  {
    "title": "Text Elements: ReStructuredText",
    "content": "Renders ReStructuredText onto the page.\n\n:param content: the ReStructuredText content to be displayed\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.restructured_text('This is **reStructuredText**.')\n\nui.run()",
    "url": "/documentation/section_text_elements#restructuredtext"
  },
  {
    "title": "Text Elements: Mermaid Diagrams",
    "content": "Renders diagrams and charts written in the Markdown-inspired `Mermaid \u003Chttps://mermaid.js.org/\u003E`_ language.\nThe mermaid syntax can also be used inside Markdown elements by providing the extension string 'mermaid' to the ``ui.markdown`` element.\n\nThe optional configuration dictionary is passed directly to mermaid before the first diagram is rendered.\nThis can be used to set such options as\n\n    ``{'securityLevel': 'loose', ...}`` - allow running JavaScript when a node is clicked\n    ``{'logLevel': 'info', ...}`` - log debug info to the console\n\nRefer to the Mermaid documentation for the ``mermaid.initialize()`` method for a full list of options.\n\n:param content: the Mermaid content to be displayed\n:param config: configuration dictionary to be passed to ``mermaid.initialize()``\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.mermaid('''\ngraph LR;\n    A --\u003E B;\n    A --\u003E C;\n''')\n\nui.run()",
    "url": "/documentation/section_text_elements#mermaid_diagrams"
  },
  {
    "title": "Text Elements: HTML Element",
    "content": "Renders arbitrary HTML onto the page, wrapped in the specified tag.\n`Tailwind \u003Chttps://v3.tailwindcss.com/\u003E`_ can be used for styling.\nYou can also use `ui.add_head_html` to add html code into the head of the document and `ui.add_body_html`\nto add it into the body.\n\n:param content: the HTML code to be displayed\n:param tag: the HTML tag to wrap the content in (default: \"div\")\n",
    "format": "rst",
    "demo": "from nicegui import ui\n\nui.html('This is \u003Cstrong\u003EHTML\u003C/strong\u003E.')\n\nui.run()",
    "url": "/documentation/section_text_elements#html_element"
  },
  {
    "title": "Text Elements: Other HTML Elements",
    "content": "There is also an `html` module that allows you to insert other HTML elements like `\u003Cspan\u003E`, `\u003Cdiv\u003E`, `\u003Cp\u003E`, etc.\nIt is equivalent to using the `ui.element` method with the `tag` argument.\n\nLike with any other element, you can add classes, style, props, tooltips and events.\nOne convenience is that the keyword arguments are automatically added to the element's `props` dictionary.\n\n*Added in version 2.5.0*",
    "format": "md",
    "demo": "from nicegui import html, ui\n\nwith html.section().style('font-size: 120%'):\n    html.strong('This is bold.') \\\n        .classes('cursor-pointer') \\\n        .on('click', lambda: ui.notify('Bold!'))\n    html.hr()\n    html.em('This is italic.').tooltip('Nice!')\n    with ui.row():\n        html.img().props('src=https://placehold.co/60')\n        html.img(src='https://placehold.co/60')\n\nui.run()",
    "url": "/documentation/section_text_elements#other_html_elements"
  },
  {
    "title": "NiceGUI Documentation: Overview",
    "content": "\n    NiceGUI is an open-source Python library to write graphical user interfaces which run in the browser.\n    It has a very gentle learning curve while still offering the option for advanced customizations.\n    NiceGUI follows a backend-first philosophy:\n    It handles all the web development details.\n    You can focus on writing Python code.\n    This makes it ideal for a wide range of projects including short\n    scripts, dashboards, robotics projects, IoT solutions, smart home automation, and machine learning.\n",
    "format": "md",
    "demo": "",
    "url": "/documentation/#overview"
  },
  {
    "title": "NiceGUI Documentation: How to use this guide",
    "content": "\n    This documentation explains how to use NiceGUI.\n    Each of the tiles covers a NiceGUI topic in detail.\n    It is recommended to start by reading this entire introduction page, then refer to other sections as needed.\n",
    "format": "md",
    "demo": "",
    "url": "/documentation/#how_to_use_this_guide"
  },
  {
    "title": "NiceGUI Documentation: Basic concepts",
    "content": "\n    NiceGUI provides UI _elements_ such as buttons, sliders, text, images, charts, and more.\n    Your app assembles these components into _pages_.\n    When the user interacts with an item on a page, NiceGUI triggers an _event_ (or _action_).\n    You define code to _handle_ each event, such as what to do when a user clicks a button, modifies a value or operates a slider.\n    Elements can also be bound to a _model_ (data object), which automatically updates the user interface when the model value changes.\n\n    Elements are arranged on a page using a \"declarative UI\" or \"code-based UI\".\n    That means that you also write structures like grids, cards, tabs, carousels, expansions, menus, and other layout elements directly in code.\n    This concept has been made popular with Flutter and SwiftUI.\n    For readability, NiceGUI utilizes Python's `with ...` statement.\n    This context manager provides a nice way to indent the code to resemble the layout of the UI.\n\n    Styling and appearance can be controlled in several ways.\n    Most elements accept optional arguments for common styling and behavior changes, such as button icons or text color.\n    Because NiceGUI is a web framework, you can change almost any appearance of an element with CSS.\n    But elements also provide `.classes` and `.props` methods to apply Tailwind CSS and Quasar properties\n    which are more high-level and simpler to use day-to-day after you get the hang of it.\n",
    "format": "md",
    "demo": "",
    "url": "/documentation/#basic_concepts"
  },
  {
    "title": "NiceGUI Documentation: Actions, Events and Tasks",
    "content": "\n    NiceGUI uses an async/await event loop for concurrency which is resource-efficient and has the great benefit of not having to worry about thread safety.\n    This section shows how to handle user input and other events like timers and keyboard bindings.\n    It also describes helper functions to wrap long-running tasks in asynchronous functions to keep the UI responsive.\n    Keep in mind that all UI updates must happen on the main thread with its event loop.\n",
    "format": "md",
    "demo": "",
    "url": "/documentation/#actions__events_and_tasks"
  },
  {
    "title": "NiceGUI Documentation: Implementation",
    "content": "\n    NiceGUI is implemented with HTML components served by an HTTP server (FastAPI), even for native windows.\n    If you already know HTML, everything will feel very familiar.\n    If you don't know HTML, that's fine too!\n    NiceGUI abstracts away the details, so you can focus on creating beautiful interfaces without worrying about how they are implemented.\n",
    "format": "md",
    "demo": "",
    "url": "/documentation/#implementation"
  },
  {
    "title": "NiceGUI Documentation: Running NiceGUI Apps",
    "content": "\n    There are several options for deploying NiceGUI.\n    By default, NiceGUI runs a server on localhost and runs your app as a private web page on the local machine.\n    When run this way, your app appears in a web browser window.\n    You can also run NiceGUI in a native window separate from a web browser.\n    Or you can run NiceGUI on a server that handles many clients - the website you're reading right now is served from NiceGUI.\n\n    After creating your app pages with components, you call `ui.run()` to start the NiceGUI server.\n    Optional parameters to `ui.run` set things like the network address and port the server binds to,\n    whether the app runs in native mode, initial window size, and many other options.\n    The section _Configuration and Deployment_ covers the options to the `ui.run()` function and the FastAPI framework it is based on.\n",
    "format": "md",
    "demo": "",
    "url": "/documentation/#running_nicegui_apps"
  },
  {
    "title": "NiceGUI Documentation: Customization",
    "content": "\n    If you want more customization in your app, you can use the underlying Tailwind classes and Quasar components\n    to control the style or behavior of your components.\n    You can also extend the available components by subclassing existing NiceGUI components or importing new ones from Quasar.\n    All of this is optional.\n    Out of the box, NiceGUI provides everything you need to make modern, stylish, responsive user interfaces.\n",
    "format": "md",
    "demo": "",
    "url": "/documentation/#customization"
  },
  {
    "title": "NiceGUI Documentation: Testing",
    "content": "\n    NiceGUI provides a comprehensive testing framework based on [pytest](https://docs.pytest.org/)\n    which allows you to automate the testing of your user interface.\n    You can utilize the `screen` fixture which starts a real (headless) browser to interact with your application.\n    This is great if you have browser-specific behavior to test.\n\n    But most of the time, NiceGUI's newly introduced `user` fixture is more suited:\n    It only simulates the user interaction on a Python level and, hence, is blazing fast.\n    That way the classical [test pyramid](https://martinfowler.com/bliki/TestPyramid.html),\n    where UI tests are considered slow and expensive, does not apply anymore.\n    This can have a huge impact on your development speed, quality and confidence.\n",
    "format": "md",
    "demo": "",
    "url": "/documentation/#testing"
  },
  {
    "title": "NiceGUI Documentation: None",
    "content": "",
    "format": "md",
    "demo": "",
    "url": "/documentation/#None"
  }
]