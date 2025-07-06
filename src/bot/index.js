import fs from 'fs';
import { Client, GatewayIntentBits, Collection } from 'discord.js';
import IntelliPHPHandler from './handlers/intelliphp-handler.js';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent,
        GatewayIntentBits.GuildMessageTyping,
    ],
});

// Initialize IntelliPHP
const intelliPHPHandler = new IntelliPHPHandler();
console.log('✅ IntelliPHP feature enabled');

// Register commands
client.commands = new Collection();
const commandsPath = join(__dirname, 'commands');
const commandFiles = fs.readdirSync(commandsPath).filter(file => file.endsWith('.js'));

for (const file of commandFiles) {
    const filePath = join(commandsPath, file);
    const command = await import(filePath);
    client.commands.set(command.default.data.name, command.default);
}

// Register IntelliPHP commands
intelliPHPHandler.registerCommands(client);

client.on('interactionCreate', async interaction => {
    if (!interaction.isChatInputCommand()) return;

    // Check if it's an IntelliPHP command
    if (await intelliPHPHandler.handleInteraction(interaction)) {
        return;
    }

    const command = client.commands.get(interaction.commandName);
    
    if (!command) return;

    try {
        await command.execute(interaction);
    } catch (error) {
        console.error(error);
        // Handle error appropriately
    }
});

// ...existing code...