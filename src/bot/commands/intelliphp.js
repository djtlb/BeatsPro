const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');
const fs = require('fs').promises;
const path = require('path');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('intelliphp')
        .setDescription('IntelliPHP AI Autocomplete for PHP')
        .addSubcommand(subcommand =>
            subcommand
                .setName('info')
                .setDescription('Get information about IntelliPHP')
        )
        .addSubcommand(subcommand =>
            subcommand
                .setName('setup')
                .setDescription('Setup instructions for IntelliPHP')
        )
        .addSubcommand(subcommand =>
            subcommand
                .setName('troubleshoot')
                .setDescription('Troubleshooting guide for IntelliPHP')
        ),

    async execute(interaction) {
        const subcommand = interaction.options.getSubcommand();

        switch (subcommand) {
            case 'info':
                await this.handleInfo(interaction);
                break;
            case 'setup':
                await this.handleSetup(interaction);
                break;
            case 'troubleshoot':
                await this.handleTroubleshoot(interaction);
                break;
        }
    },

    async handleInfo(interaction) {
        const embed = new EmbedBuilder()
            .setColor('#0099ff')
            .setTitle('🧠 IntelliPHP - AI Autocomplete for PHP')
            .setDescription('Advanced AI-assisted development tool for PHP programmers')
            .addFields(
                { name: '🚀 Key Features', value: '• AI Auto-completion\n• Code Snippets\n• Framework Support\n• Local Processing\n• CPU Optimized', inline: true },
                { name: '⚡ Performance', value: '• No GPU required\n• Zero latency\n• Secure & Private\n• Works offline', inline: true },
                { name: '🔧 Frameworks', value: '• Laravel\n• WordPress\n• Drupal\n• Custom PHP', inline: true }
            )
            .setFooter({ text: 'IntelliPHP keeps your code secure and private' });

        await interaction.reply({ embeds: [embed] });
    },

    async handleSetup(interaction) {
        const embed = new EmbedBuilder()
            .setColor('#00ff00')
            .setTitle('⚙️ IntelliPHP Setup Guide')
            .addFields(
                { name: '1. Installation', value: '```\nInstall DEVSENSE.intelli-php-vscode extension\n```' },
                { name: '2. Configuration', value: '```json\n{\n  "intelliphp.inlineSuggestionsEnabled": true,\n  "editor.inlineSuggest.enabled": true\n}\n```' },
                { name: '3. Usage', value: '• Press **TAB** to accept suggestions\n• **Ctrl + Right Arrow** for word completion\n• Continue typing to dismiss suggestions' },
                { name: '4. Keyboard Shortcuts', value: '• `TAB` - Accept suggestion\n• `TAB` (again) - Complete snippet\n• `Ctrl + →` - Accept word' }
            );

        await interaction.reply({ embeds: [embed] });
    },

    async handleTroubleshoot(interaction) {
        const embed = new EmbedBuilder()
            .setColor('#ff9900')
            .setTitle('🔧 IntelliPHP Troubleshooting')
            .addFields(
                { name: '📋 Check Settings', value: '• Verify `editor.inlineSuggest.enabled` is `true`\n• Ensure IntelliPHP extension is enabled' },
                { name: '📊 Logs & Diagnostics', value: '• Check OUTPUT → "IntelliPHP" tab\n• Run `IntelliPHP: About...` command' },
                { name: '🔄 Common Fixes', value: '• Restart VSCode\n• Reload window (Ctrl+Shift+P)\n• Check extension permissions' },
                { name: '💡 Performance Tips', value: '• Close unused PHP files\n• Disable other autocomplete extensions\n• Ensure sufficient RAM available' }
            );

        await interaction.reply({ embeds: [embed] });
    }
};
