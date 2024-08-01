from nicegui import ui

def create_responsive_card(title, content):
    # with ui.card().classes('w-full sm:w-1/2 md:w-1/3 lg:w-1/4 m-2 p-4 bg-white dark:bg-gray-800 shadow-lg rounded-lg transition duration-300 ease-in-out hover:shadow-xl'):
    with ui.card().classes('bg-gradient-to-r from-cyan-500 to-blue-500 border-2 border-gray-300 rounded-xl p-4'):
        ui.label(title).classes('text-xl font-bold mb-2 text-gray-800 dark:text-white')
        ui.label(content).classes('text-gray-600 dark:text-gray-300')
        ui.button('Learn More').classes('mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded')
        ui.button('Hover Me').classes('transition duration-300 ease-in-out transform hover:scale-110')


with ui.row().classes('space-x-2'):
    for i in range(3):
        ui.button(f'Button {i+1}').classes('first:bg-green-500 last:bg-red-500')

with ui.row().classes('flex flex-wrap justify-center'):
    create_responsive_card('Card 1', 'This is the content for card 1.')
    create_responsive_card('Card 2', 'This is the content for card 2.')
    create_responsive_card('Card 3', 'This is the content for card 3.')

ui.run()
