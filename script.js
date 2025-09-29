// Game Constants
const SCREEN_WIDTH = 288;
const SCREEN_HEIGHT = 512;
const GRAVITY = 0.25;
const FLAP_POWER = -5;
const PIPE_SPACING = 200;

// Game States
const GameState = {
    HOME: 'HOME',
    PLAYING: 'PLAYING',
    GAME_OVER: 'GAME_OVER',
    SHOP: 'SHOP',
    CONFIRM_RESET: 'CONFIRM_RESET',
    BACKGROUND_SHOP: 'BACKGROUND_SHOP',
    POWER_SHOP: 'POWER_SHOP',
    PARTICLES_SHOP: 'PARTICLES_SHOP',
    MUSIC_SHOP: 'MUSIC_SHOP'
};

// Difficulty Settings
const Difficulty = {
    EASY: { gap: 150, speed: 2, name: 'EASY' },
    NORMAL: { gap: 120, speed: 2.5, name: 'NORMAL' },
    HARD: { gap: 90, speed: 3, name: 'HARD' }
};

// Game Classes
class Bird {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.velocity = 0;
        this.width = 34;
        this.height = 24;
        this.animationTimer = 0;
        this.animationSpeed = 0.2;
        this.currentFrame = 1;
        this.animationSequence = [0, 1, 2, 1];
        this.animationIndex = 0;
        this.lastUpdate = Date.now();
        this.images = {}; // Will store loaded images for different skins
    }

    flap() {
        this.velocity = FLAP_POWER;
    }

    update(deltaTime = 1/60) {
        this.velocity += GRAVITY;
        this.y += this.velocity;

        // Update wing animation using delta time
        this.animationTimer += deltaTime;
        if (this.animationTimer >= this.animationSpeed) {
            this.animationIndex = (this.animationIndex + 1) % this.animationSequence.length;
            this.currentFrame = this.animationSequence[this.animationIndex];
            this.animationTimer = 0;
        }
    }

    draw(ctx, skin, assets) {
        // Use actual bird sprites if available
        const skinImages = assets.birdImages[skin];
        if (skinImages && skinImages[this.currentFrame]) {
            const image = skinImages[this.currentFrame];
            ctx.drawImage(image, this.x, this.y, this.width, this.height);
        } else {
            // Fallback to colored rectangles
            const colors = {
                default: '#FFD700',
                blue: '#4287F5',
                red: '#F54242',
                golden: '#FFD700'
            };

            ctx.fillStyle = colors[skin] || colors.default;
            ctx.fillRect(this.x, this.y, this.width, this.height);

            // Simple wing animation
            ctx.fillStyle = '#000';
            const wingOffset = this.currentFrame === 0 ? -2 : this.currentFrame === 2 ? 2 : 0;
            ctx.fillRect(this.x + 5, this.y + 5 + wingOffset, 10, 5);
        }
    }

    getRect() {
        return { x: this.x, y: this.y, width: this.width, height: this.height };
    }
}

class Pipe {
    constructor(x, difficulty, pipeHeight = 320) {
        this.x = x;
        this.pipeHeight = pipeHeight;
        this.setDifficulty(difficulty);
        this.passed = false;
        this.width = 52;
    }

    setDifficulty(difficulty) {
        this.difficulty = difficulty;
        this.speed = difficulty.speed;
        this.gap = difficulty.gap;
        this.gapY = Math.random() * (SCREEN_HEIGHT - this.gap - 200) + 100;
    }

    update(deltaTime = 1/60) {
        this.x -= this.speed * (deltaTime * 60); // Normalize speed to 60fps
    }

    draw(ctx, assets) {
        if (assets.pipeImage) {
            // Draw top pipe (flipped)
            ctx.save();
            ctx.scale(1, -1);
            ctx.drawImage(assets.pipeImage, this.x, -(this.gapY), this.width, this.pipeHeight);
            ctx.restore();

            // Draw bottom pipe (normal)
            ctx.drawImage(assets.pipeImage, this.x, this.gapY + this.gap, this.width, this.pipeHeight);
        } else {
            // Fallback to green rectangles
            ctx.fillStyle = '#00FF00';
            // Top pipe
            ctx.fillRect(this.x, this.gapY - this.pipeHeight, this.width, this.pipeHeight);
            // Bottom pipe
            ctx.fillRect(this.x, this.gapY + this.gap, this.width, this.pipeHeight);
        }
    }

    getTopRect() {
        return {
            x: this.x,
            y: this.gapY - this.pipeHeight,
            width: this.width,
            height: this.pipeHeight
        };
    }

    getBottomRect() {
        return {
            x: this.x,
            y: this.gapY + this.gap,
            width: this.width,
            height: this.pipeHeight
        };
    }
}

class Particle {
    constructor(x, y, type) {
        this.x = x;
        this.y = y;
        this.type = type;
        this.life = 1.0;
        this.age = 0.0;

        if (type === 'stars') {
            this.velocityX = (Math.random() - 0.5) * 2;
            this.velocityY = (Math.random() - 0.5) * 2;
            this.size = Math.random() * 2 + 2;
            this.color = `rgb(255, 255, ${Math.floor(Math.random() * 105 + 150)})`;
            this.decayRate = 0.02;
        } else if (type === 'fire') {
            this.velocityX = (Math.random() - 0.5);
            this.velocityY = Math.random() * -2;
            this.size = Math.random() * 3 + 3;
            this.color = `rgb(255, ${Math.floor(Math.random() * 50 + 100)}, 0)`;
            this.decayRate = 0.03;
        } else if (type === 'sparkles') {
            this.velocityX = (Math.random() - 0.5) * 3;
            this.velocityY = (Math.random() - 0.5) * 3;
            this.size = Math.random() * 2 + 1;
            const colors = ['rgb(255, 192, 203)', 'rgb(138, 43, 226)', 'rgb(0, 255, 255)', 'rgb(255, 255, 0)'];
            this.color = colors[Math.floor(Math.random() * colors.length)];
            this.decayRate = 0.025;
        } else if (type === 'rainbow') {
            this.velocityX = (Math.random() - 0.5) * 1.6;
            this.velocityY = (Math.random() - 0.5) * 1.6;
            this.size = Math.random() * 3 + 2;
            this.baseHue = Math.random() * 360;
            this.decayRate = 0.015;
        }
    }

    update(deltaTime = 1/60) {
        this.x += this.velocityX * (deltaTime * 60);
        this.y += this.velocityY * (deltaTime * 60);
        this.age += deltaTime;
        this.life -= this.decayRate * (deltaTime * 60);

        if (this.type === 'rainbow') {
            const hue = (this.baseHue + this.age * 100) % 360;
            this.color = `hsl(${hue}, 100%, 50%)`;
        }

        return this.life > 0;
    }

    draw(ctx) {
        if (this.life > 0) {
            const alpha = Math.max(0, Math.min(1, this.life));
            ctx.save();
            ctx.globalAlpha = alpha;
            ctx.fillStyle = this.color;
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();
        }
    }
}

class Cloud {
    constructor() {
        this.x = Math.random() * (SCREEN_WIDTH + 200) - 100;
        this.y = Math.random() * 150 + 50;
        this.speed = Math.random() * 0.7 + 0.3;
        this.size = Math.random() * 40 + 40;
        this.opacity = Math.random() * 0.6 + 0.4;
    }

    update(deltaTime = 1/60) {
        this.x += this.speed * (deltaTime * 60);
    }

    draw(ctx) {
        ctx.save();
        ctx.globalAlpha = this.opacity;
        ctx.fillStyle = '#FFF';

        // Draw cloud as overlapping circles
        for (let i = 0; i < 5; i++) {
            const offsetX = i * (this.size / 5);
            const offsetY = Math.sin(i) * 3;
            const radius = this.size / 5 + Math.random() * 5;

            ctx.beginPath();
            ctx.arc(this.x + offsetX, this.y + offsetY, radius, 0, Math.PI * 2);
            ctx.fill();
        }

        ctx.restore();
    }
}

// Asset Loading System
class AssetLoader {
    constructor() {
        this.assets = {
            birdImages: {},
            pipeImage: null,
            backgroundImage: null,
            sounds: {},
            music: {},
            numberImages: {},
            gameOverImage: null
        };
        this.loaded = false;
        this.loadPromises = [];
    }

    loadImage(src) {
        return new Promise((resolve, reject) => {
            const img = new Image();
            img.onload = () => resolve(img);
            img.onerror = reject;
            img.src = src;
        });
    }

    loadAudio(src) {
        return new Promise((resolve, reject) => {
            const audio = new Audio();

            // Set up multiple event handlers for better compatibility
            const onLoad = () => {
                console.log(`Audio loaded successfully: ${src}`);
                cleanup();
                resolve(audio);
            };

            const onError = (error) => {
                console.error(`Failed to load audio: ${src}`, error);
                cleanup();
                reject(error);
            };

            const cleanup = () => {
                audio.removeEventListener('canplaythrough', onLoad);
                audio.removeEventListener('loadeddata', onLoad);
                audio.removeEventListener('error', onError);
            };

            // Try multiple load events for better browser compatibility
            audio.addEventListener('canplaythrough', onLoad);
            audio.addEventListener('loadeddata', onLoad);
            audio.addEventListener('error', onError);

            // Set audio properties for better performance
            audio.preload = 'auto';
            audio.src = src;
        });
    }

    setupMusicTrack(audio, musicId) {
        // Set up music properties
        audio.loop = true;
        audio.preload = 'auto';

        // Apply different audio characteristics for each track
        switch(musicId) {
            case 'default':
                audio.volume = 0.3;
                audio.playbackRate = 1.0;
                break;
            case 'classic':
                audio.volume = 0.35;
                audio.playbackRate = 0.9; // Slightly slower, more retro feel
                break;
            case 'ambient':
                audio.volume = 0.2; // Quieter, more ambient
                audio.playbackRate = 0.8; // Much slower, dreamy
                break;
            case 'electronic':
                audio.volume = 0.4; // Louder, more energetic
                audio.playbackRate = 1.15; // Faster, more upbeat
                break;
            case 'peaceful':
                audio.volume = 0.25; // Quiet and peaceful
                audio.playbackRate = 0.85; // Slower, more relaxing
                break;
            default:
                audio.volume = 0.3;
                audio.playbackRate = 1.0;
        }

        // Add event listeners (these will be handled by the Game class)
        audio.addEventListener('play', () => {
            console.log(`Music ${musicId} started playing (rate: ${audio.playbackRate}, volume: ${audio.volume})`);
        });
        audio.addEventListener('pause', () => {
            console.log(`Music ${musicId} paused`);
        });
        audio.addEventListener('error', (e) => {
            console.error(`Music ${musicId} error:`, e);
        });
    }

    async loadAssets() {
        try {
            // Load bird animations for each skin
            const skins = ['default', 'blue', 'red', 'golden'];
            const frames = ['up', 'middle', 'down'];

            for (const skin of skins) {
                this.assets.birdImages[skin] = [];
                for (let i = 0; i < frames.length; i++) {
                    const frame = frames[i];
                    let imagePath;
                    if (skin === 'default') {
                        imagePath = `assets/bird_${frame}.png`;
                    } else {
                        imagePath = `assets/skins/bird_${skin}_${frame}.png`;
                    }
                    const img = await this.loadImage(imagePath);
                    this.assets.birdImages[skin][i] = img;
                }
            }

            // Load other assets
            this.assets.pipeImage = await this.loadImage('assets/pipe.png');
            this.assets.backgroundImage = await this.loadImage('assets/background.png');

            // Load sounds
            this.assets.sounds.wing = await this.loadAudio('sounds/wing.wav');

            // Load all music tracks
            const musicFiles = {
                default: 'sounds/background-music.mp3',
                classic: 'sounds/classic.mp3',
                ambient: 'sounds/ambient.mp3',
                electronic: 'sounds/electronic.mp3',
                peaceful: 'sounds/peaceful.mp3'
            };

            for (const [musicId, filePath] of Object.entries(musicFiles)) {
                try {
                    this.assets.music[musicId] = await this.loadAudio(filePath);
                    this.setupMusicTrack(this.assets.music[musicId], musicId);
                    console.log(`Loaded music track: ${musicId}`);
                } catch (error) {
                    console.warn(`Failed to load music track ${musicId}:`, error);
                    // Continue loading other tracks even if one fails
                }
            }

            // Load number sprites
            for (let i = 0; i <= 9; i++) {
                this.assets.numberImages[i] = await this.loadImage(`fonts/number_${i}.png`);
            }

            this.assets.gameOverImage = await this.loadImage('fonts/game_over.png');

            this.loaded = true;
            console.log('All assets loaded successfully!');

        } catch (error) {
            console.warn('Some assets failed to load:', error);
            this.loaded = true; // Continue anyway with fallbacks
        }

        // Update music status after loading
        setTimeout(() => {
            const musicCount = Object.keys(this.assets.music).length;
            if (musicCount > 0) {
                this.updateMusicStatus(`Ready (${musicCount} tracks)`);
            } else {
                this.updateMusicStatus('No Music Available');
            }
        }, 100);
    }
}

// Main Game Class
class Game {
    constructor() {
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');

        this.assetLoader = new AssetLoader();
        this.assetsLoaded = false;

        this.bird = new Bird(50, SCREEN_HEIGHT / 2);
        this.pipes = [];
        this.particles = [];
        this.clouds = [];
        this.score = 0;
        this.coins = 0;
        this.totalCoins = 0;
        this.state = GameState.HOME;
        this.difficulty = Difficulty.NORMAL;

        // Frame rate limiting
        this.targetFPS = 60;
        this.frameInterval = 1000 / this.targetFPS;
        this.lastFrameTime = 0;
        this.deltaTime = 0;

        // Initialize clouds
        for (let i = 0; i < 5; i++) {
            this.clouds.push(new Cloud());
        }

        // Game data
        this.highScore = { EASY: 0, NORMAL: 0, HARD: 0 };
        this.currentSkin = 'default';
        this.ownedSkins = { default: true };
        this.availableSkins = {
            default: { price: 0, name: 'Default' },
            blue: { price: 50, name: 'Blue Bird' },
            red: { price: 100, name: 'Red Bird' },
            golden: { price: 200, name: 'Golden Bird' }
        };

        this.currentBackground = 'default';
        this.ownedBackgrounds = { default: true };
        this.availableBackgrounds = {
            default: { price: 0, name: 'Sky Blue', color: 'rgb(135, 206, 235)' },
            sunset: { price: 75, name: 'Sunset', color: 'rgb(255, 140, 0)' },
            night: { price: 100, name: 'Night Sky', color: 'rgb(25, 25, 112)' },
            forest: { price: 150, name: 'Forest', color: 'rgb(34, 139, 34)' },
            ocean: { price: 125, name: 'Ocean', color: 'rgb(0, 100, 140)' }
        };

        this.ownedPowers = new Set();
        this.availablePowers = {
            pipe_destroyer: {
                price: 200,
                name: 'Pipe Destroyer',
                description: 'Press X to destroy all pipes!',
                cooldown: 10.0,
                key: 'KeyX'
            },
            shield: {
                price: 300,
                name: 'Shield',
                description: 'Press Z for 3 seconds of invincibility!',
                cooldown: 15.0,
                key: 'KeyZ',
                duration: 3.0
            }
        };

        this.currentParticle = 'none';
        this.ownedParticles = { none: true };
        this.availableParticles = {
            none: { price: 0, name: 'None' },
            stars: { price: 80, name: 'Starry Trail' },
            fire: { price: 120, name: 'Fire Trail' },
            sparkles: { price: 150, name: 'Magic Sparkles' },
            rainbow: { price: 200, name: 'Rainbow Trail' }
        };

        // Music system
        this.currentMusic = 'default';
        this.ownedMusic = { default: true, none: true };
        this.availableMusic = {
            none: { price: 0, name: 'No Music', file: null, description: 'Complete silence' },
            default: { price: 0, name: 'Original Theme', file: 'sounds/background-music.mp3', description: 'Normal speed & volume' },
            classic: { price: 75, name: 'Classic Arcade', file: 'sounds/classic.mp3', description: 'Slower retro feel' },
            ambient: { price: 100, name: 'Ambient Sky', file: 'sounds/ambient.mp3', description: 'Quiet & dreamy' },
            electronic: { price: 125, name: 'Electronic Beat', file: 'sounds/electronic.mp3', description: 'Fast & energetic' },
            peaceful: { price: 150, name: 'Peaceful Garden', file: 'sounds/peaceful.mp3', description: 'Soft & relaxing' },
            funkyChiptune: { price: 200, name: 'Funky Chiptune', file: 'music/Funky-Chiptune.mp3', description: 'High energy 8-bit beats' },
            bonkersArcade: { price: 225, name: 'Bonkers for Arcades', file: 'music/Bonkers-for-Arcades.mp3', description: 'Retro arcade vibes' },
            arcadePuzzler: { price: 175, name: 'Arcade Puzzler', file: 'music/Arcade-Puzzler.mp3', description: 'Classic 80s arcade sound' },
            bitPerplexion: { price: 250, name: '8-Bit Perplexion', file: 'music/8-Bit-Perplexion.mp3', description: 'Quirky chiptune adventure' }
        };

        this.powerCooldowns = {};
        this.shieldActive = false;
        this.shieldTimer = 0.0;

        // Music management
        this.musicCheckInterval = null;
        this.lastMusicCheck = Date.now();
        this.lastMusicTime = 0;
        this.musicEnabled = true;

        this.loadSaveData();
        this.setupEventListeners();
        this.resetGame();
        this.updateUI();

        // Load assets and start game
        this.initGame();
    }

    isMobile() {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    }

    async initGame() {
        console.log('Initializing game...');

        // Show loading message
        this.ctx.fillStyle = '#87CEEB';
        this.ctx.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
        this.ctx.fillStyle = '#000';
        this.ctx.font = '16px monospace';
        this.ctx.textAlign = 'center';
        this.ctx.fillText('Loading...', SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2);

        // Load all assets
        await this.assetLoader.loadAssets();
        this.assetsLoaded = true;
        console.log('Assets loaded, game ready');

        // Handle music differently on mobile vs desktop
        if (this.isMobile()) {
            console.log('Mobile device detected - music will start on user interaction');
            this.updateMusicStatus('Ready');
        } else {
            // Start background music based on current selection (desktop only)
            try {
                console.log(`Attempting to start music: ${this.currentMusic}`);
                if (this.currentMusic !== 'none') {
                    const music = this.getCurrentMusic();
                    if (music) {
                        const playPromise = music.play();
                        if (playPromise !== undefined) {
                            await playPromise;
                            console.log('Background music started successfully');
                            this.updateMusicStatus('Playing');
                        }
                    } else {
                        console.log('Music track not found, falling back to default');
                        this.currentMusic = 'default';
                        this.saveGameData();
                    }
                } else {
                    this.updateMusicStatus('No Music');
                }
            } catch (error) {
                console.log('Background music autoplay blocked - will start on first user interaction:', error.message);
                this.updateMusicStatus('Ready');
            }
        }

        // Start background music monitoring
        this.startMusicMonitoring();

        // Start game loop
        this.gameLoop();
    }

    loadSaveData() {
        try {
            const data = JSON.parse(localStorage.getItem('flappyBirdSave') || '{}');
            this.highScore = data.highScore || { EASY: 0, NORMAL: 0, HARD: 0 };
            this.totalCoins = data.totalCoins || 0;
            this.ownedSkins = data.ownedSkins || { default: true };
            this.currentSkin = data.currentSkin || 'default';
            this.ownedBackgrounds = data.ownedBackgrounds || { default: true };
            this.currentBackground = data.currentBackground || 'default';
            this.ownedPowers = new Set(data.ownedPowers || []);
            this.ownedParticles = data.ownedParticles || { none: true };
            this.currentParticle = data.currentParticle || 'none';
            this.ownedMusic = data.ownedMusic || { default: true, none: true };
            this.currentMusic = data.currentMusic || 'default';
        } catch (e) {
            console.log('Could not load save data');
            // Set default values including test coins
            this.highScore = { EASY: 0, NORMAL: 0, HARD: 0 };
            this.totalCoins = 0;
            this.ownedSkins = { default: true };
            this.currentSkin = 'default';
            this.ownedBackgrounds = { default: true };
            this.currentBackground = 'default';
            this.ownedPowers = new Set();
            this.ownedParticles = { none: true };
            this.currentParticle = 'none';
            this.ownedMusic = { default: true, none: true };
            this.currentMusic = 'default';
        }
    }

    saveGameData() {
        const data = {
            highScore: this.highScore,
            totalCoins: this.totalCoins,
            ownedSkins: this.ownedSkins,
            currentSkin: this.currentSkin,
            ownedBackgrounds: this.ownedBackgrounds,
            currentBackground: this.currentBackground,
            ownedPowers: Array.from(this.ownedPowers),
            ownedParticles: this.ownedParticles,
            currentParticle: this.currentParticle,
            ownedMusic: this.ownedMusic,
            currentMusic: this.currentMusic
        };
        localStorage.setItem('flappyBirdSave', JSON.stringify(data));
    }

    resetAllData() {
        this.highScore = { EASY: 0, NORMAL: 0, HARD: 0 };
        this.totalCoins = 0;
        this.ownedSkins = { default: true };
        this.currentSkin = 'default';
        this.ownedBackgrounds = { default: true };
        this.currentBackground = 'default';
        this.ownedPowers = new Set();
        this.ownedParticles = { none: true };
        this.currentParticle = 'none';
        this.ownedMusic = { default: true, none: true };
        this.currentMusic = 'default';
        this.score = 0;
        this.saveGameData();
    }

    resetCoinsOnly() {
        // Only reset coins, keep all other progress
        this.totalCoins = 0;
        this.score = 0;
        this.saveGameData();
    }

    setupEventListeners() {
        // Keyboard events
        document.addEventListener('keydown', (e) => this.handleKeyDown(e));

        // UI button events
        document.getElementById('shopBtn').addEventListener('click', () => {
            this.tryPlayBackgroundMusic();
            this.setState(GameState.SHOP);
        });
        document.getElementById('newGameBtn').addEventListener('click', () => {
            this.tryPlayBackgroundMusic();
            this.setState(GameState.CONFIRM_RESET);
        });
        document.getElementById('homeBtn').addEventListener('click', () => {
            this.tryPlayBackgroundMusic();
            this.resetGame(false);
        });
        document.getElementById('shopBackBtn').addEventListener('click', () => {
            this.tryPlayBackgroundMusic();
            this.setState(GameState.HOME);
        });

        // Shop navigation
        document.getElementById('backgroundsBtn').addEventListener('click', () => this.setState(GameState.BACKGROUND_SHOP));
        document.getElementById('powersBtn').addEventListener('click', () => this.setState(GameState.POWER_SHOP));
        document.getElementById('particlesBtn').addEventListener('click', () => this.setState(GameState.PARTICLES_SHOP));
        document.getElementById('musicBtn').addEventListener('click', () => this.setState(GameState.MUSIC_SHOP));

        // Shop back buttons
        document.getElementById('bgBackBtn').addEventListener('click', () => this.setState(GameState.SHOP));
        document.getElementById('powerBackBtn').addEventListener('click', () => this.setState(GameState.SHOP));
        document.getElementById('particleBackBtn').addEventListener('click', () => this.setState(GameState.SHOP));
        document.getElementById('musicBackBtn').addEventListener('click', () => this.setState(GameState.SHOP));

        // Confirm reset
        document.getElementById('confirmYes').addEventListener('click', () => {
            this.resetAllData();
            this.setState(GameState.HOME);
            this.updateUI();
        });
        document.getElementById('confirmNo').addEventListener('click', () => this.setState(GameState.HOME));

        // Difficulty selection
        document.querySelectorAll('.difficulty-option').forEach(option => {
            option.addEventListener('click', () => {
                const diff = option.dataset.difficulty;
                this.difficulty = Difficulty[diff];

                // Try to start background music on mobile
                if (this.isMobile()) {
                    this.tryPlayBackgroundMusic();
                }

                this.resetGame(true);
            });
        });

        // Canvas click for flapping
        this.canvas.addEventListener('click', () => {
            if (this.state === GameState.PLAYING) {
                this.bird.flap();
                this.generateParticles();
                this.playSound('wing');
            } else if (this.state === GameState.GAME_OVER) {
                this.resetGame(true);
            }

            // Try to start background music on first user interaction
            this.tryPlayBackgroundMusic();
        });

        // Music status click handler
        document.getElementById('musicStatus').addEventListener('click', () => {
            this.toggleBackgroundMusic();
        });

        // Cleanup on page unload
        window.addEventListener('beforeunload', () => {
            if (this.musicCheckInterval) {
                clearInterval(this.musicCheckInterval);
            }
        });
    }

    handleKeyDown(e) {
        // Try to start background music on any key press
        this.tryPlayBackgroundMusic();

        if (e.code === 'Escape' && this.state !== GameState.HOME) {
            this.resetGame(false);
            return;
        }

        if (this.state === GameState.HOME) {
            if (e.code === 'Digit1') {
                this.difficulty = Difficulty.EASY;
                this.resetGame(true);
            } else if (e.code === 'Digit2') {
                this.difficulty = Difficulty.NORMAL;
                this.resetGame(true);
            } else if (e.code === 'Digit3') {
                this.difficulty = Difficulty.HARD;
                this.resetGame(true);
            }
        } else if (this.state === GameState.PLAYING) {
            if (e.code === 'Space' || e.code === 'ArrowUp') {
                e.preventDefault();
                this.bird.flap();
                this.generateParticles();
                this.playSound('wing');
            }

            // Handle power keys
            for (const [powerId, powerData] of Object.entries(this.availablePowers)) {
                if (this.ownedPowers.has(powerId) && e.code === powerData.key) {
                    if (!this.powerCooldowns[powerId]) {
                        this.usePower(powerId);
                    }
                }
            }
        } else if (this.state === GameState.GAME_OVER) {
            if (e.code === 'Space') {
                this.resetGame(true);
            } else if (e.code === 'KeyH') {
                this.resetGame(false);
            }
        }
    }

    updateMusicStatus(status) {
        const musicStatusEl = document.getElementById('musicStatus');
        if (musicStatusEl) {
            musicStatusEl.textContent = `🎵 Music: ${status}`;
        }
    }

    playSound(soundName) {
        if (this.assetsLoaded && this.assetLoader.assets.sounds[soundName]) {
            try {
                const sound = this.assetLoader.assets.sounds[soundName].cloneNode();
                sound.volume = soundName === 'wing' ? 0.5 : 0.3;
                sound.play();
            } catch (error) {
                console.log('Could not play sound:', soundName);
            }
        }
    }

    tryPlayBackgroundMusic() {
        if (this.currentMusic === 'none') return;

        const music = this.getCurrentMusic();
        if (music && music.paused) {
            try {
                console.log('Starting background music after user interaction...');
                // Set volume lower for mobile devices
                if (this.isMobile()) {
                    music.volume = Math.min(music.volume, 0.2);
                }

                music.play().then(() => {
                    console.log('Background music started successfully after user interaction');
                    this.updateMusicStatus('Playing');
                }).catch(error => {
                    console.log('Could not start background music:', error.message);
                    // On mobile, don't show error - just mark as ready
                    this.updateMusicStatus(this.isMobile() ? 'Ready' : 'Blocked');
                });
            } catch (error) {
                console.log('Could not start background music:', error.message);
                this.updateMusicStatus(this.isMobile() ? 'Ready' : 'Error');
            }
        }
    }

    startMusicMonitoring() {
        // Check music status every 2 seconds
        this.musicCheckInterval = setInterval(() => {
            this.checkMusicStatus();
        }, 2000);
    }

    checkMusicStatus() {
        if (!this.assetsLoaded || this.currentMusic === 'none') return;

        const music = this.getCurrentMusic();
        if (!music) return;

        const now = Date.now();

        // If music should be playing but isn't, try to restart it
        if (music.paused && this.state === GameState.PLAYING) {
            console.log('Music unexpectedly paused, attempting to restart...');
            this.tryPlayBackgroundMusic();
        }

        // Check if current time hasn't advanced (music might be stuck)
        if (!music.paused && music.currentTime === this.lastMusicTime && now - this.lastMusicCheck > 3000) {
            console.log('Music appears stuck, restarting...');
            music.currentTime = 0;
            music.play().catch(error => {
                console.log('Could not restart stuck music:', error.message);
            });
        }

        this.lastMusicTime = music.currentTime;
        this.lastMusicCheck = now;
    }

    switchMusic(musicId) {
        console.log(`Switching to music: ${musicId}`);

        // Stop current music
        this.stopAllMusic();

        // Update current music selection
        this.currentMusic = musicId;
        this.saveGameData();

        // Start new music if not 'none'
        if (musicId !== 'none' && this.assetsLoaded) {
            const music = this.assetLoader.assets.music[musicId];
            if (music) {
                music.currentTime = 0; // Reset to beginning
                music.play().then(() => {
                    console.log(`Successfully started playing: ${musicId}`);
                    this.updateMusicStatus('Playing');
                }).catch(error => {
                    console.log(`Could not play music ${musicId}:`, error.message);
                    this.updateMusicStatus('Blocked');
                });
            } else {
                console.warn(`Music track ${musicId} not found`);
                this.updateMusicStatus('Not Found');
            }
        } else {
            this.updateMusicStatus('No Music');
        }
    }

    stopAllMusic() {
        if (this.assetsLoaded && this.assetLoader.assets.music) {
            for (const [musicId, music] of Object.entries(this.assetLoader.assets.music)) {
                if (music && !music.paused) {
                    music.pause();
                    music.currentTime = 0;
                }
            }
        }
    }

    getCurrentMusic() {
        if (this.currentMusic === 'none' || !this.assetsLoaded) {
            return null;
        }
        return this.assetLoader.assets.music[this.currentMusic];
    }

    toggleBackgroundMusic() {
        const music = this.getCurrentMusic();
        if (music) {
            if (music.paused) {
                music.play().catch(error => {
                    console.log('Could not play music:', error.message);
                    this.updateMusicStatus('Blocked');
                });
            } else {
                music.pause();
            }
        } else if (this.currentMusic === 'none') {
            // Switch to default music
            this.switchMusic('default');
        }
    }

    usePower(powerId) {
        const powerData = this.availablePowers[powerId];

        if (powerId === 'pipe_destroyer') {
            this.pipes = [];
            this.powerCooldowns[powerId] = powerData.cooldown;
        } else if (powerId === 'shield') {
            this.shieldActive = true;
            this.shieldTimer = powerData.duration;
            this.powerCooldowns[powerId] = powerData.cooldown;
        }
    }

    generateParticles() {
        if (this.currentParticle !== 'none') {
            for (let i = 0; i < 3; i++) {
                const particleX = this.bird.x + (Math.random() - 0.5) * 20;
                const particleY = this.bird.y + (Math.random() - 0.5) * 20 + 12;
                this.particles.push(new Particle(particleX, particleY, this.currentParticle));
            }
        }
    }

    setState(newState) {
        this.state = newState;

        // Hide all screens
        document.querySelectorAll('.screen').forEach(screen => {
            screen.style.display = 'none';
        });

        // Show appropriate screen
        switch (newState) {
            case GameState.HOME:
                document.getElementById('homeScreen').style.display = 'flex';
                document.getElementById('gameUI').style.display = 'none';
                break;
            case GameState.PLAYING:
                document.getElementById('gameUI').style.display = 'block';
                break;
            case GameState.GAME_OVER:
                document.getElementById('gameOverScreen').style.display = 'flex';
                document.getElementById('gameUI').style.display = 'none';
                break;
            case GameState.SHOP:
                document.getElementById('shopScreen').style.display = 'flex';
                this.updateShopUI();
                break;
            case GameState.BACKGROUND_SHOP:
                document.getElementById('backgroundShop').style.display = 'flex';
                this.updateBackgroundShopUI();
                break;
            case GameState.POWER_SHOP:
                document.getElementById('powerShop').style.display = 'flex';
                this.updatePowerShopUI();
                break;
            case GameState.PARTICLES_SHOP:
                document.getElementById('particleShop').style.display = 'flex';
                this.updateParticleShopUI();
                break;
            case GameState.MUSIC_SHOP:
                document.getElementById('musicShop').style.display = 'flex';
                this.updateMusicShopUI();
                break;
            case GameState.CONFIRM_RESET:
                document.getElementById('confirmReset').style.display = 'flex';
                break;
        }

        this.updateUI();
    }

    updateShopUI() {
        const container = document.getElementById('skinOptions');
        container.innerHTML = '';

        for (const [skinId, skinData] of Object.entries(this.availableSkins)) {
            const button = document.createElement('button');
            button.className = 'shop-item';

            if (skinId === this.currentSkin) {
                button.classList.add('selected');
                button.textContent = `${skinData.name} - SELECTED`;
            } else if (this.ownedSkins[skinId]) {
                button.classList.add('owned');
                button.textContent = `${skinData.name} - OWNED`;
                button.addEventListener('click', () => {
                    this.currentSkin = skinId;
                    this.saveGameData();
                    this.updateShopUI();
                });
            } else {
                button.textContent = `${skinData.name} - ${skinData.price} coins`;
                button.addEventListener('click', () => {
                    if (this.totalCoins >= skinData.price) {
                        this.totalCoins -= skinData.price;
                        this.ownedSkins[skinId] = true;
                        this.currentSkin = skinId;
                        this.saveGameData();
                        this.updateShopUI();
                        this.updateUI();
                    }
                });
            }

            container.appendChild(button);
        }
    }

    updateBackgroundShopUI() {
        const container = document.getElementById('backgroundOptions');
        container.innerHTML = '';

        for (const [bgId, bgData] of Object.entries(this.availableBackgrounds)) {
            const button = document.createElement('button');
            button.className = 'shop-item';
            button.style.backgroundColor = bgData.color;

            if (bgId === this.currentBackground) {
                button.classList.add('selected');
                button.textContent = `${bgData.name} - SELECTED`;
            } else if (this.ownedBackgrounds[bgId]) {
                button.classList.add('owned');
                button.textContent = `${bgData.name} - OWNED`;
                button.addEventListener('click', () => {
                    this.currentBackground = bgId;
                    this.saveGameData();
                    this.updateBackgroundShopUI();
                });
            } else {
                button.textContent = `${bgData.name} - ${bgData.price} coins`;
                button.addEventListener('click', () => {
                    if (this.totalCoins >= bgData.price) {
                        this.totalCoins -= bgData.price;
                        this.ownedBackgrounds[bgId] = true;
                        this.currentBackground = bgId;
                        this.saveGameData();
                        this.updateBackgroundShopUI();
                        this.updateUI();
                    }
                });
            }

            container.appendChild(button);
        }
    }

    updatePowerShopUI() {
        const container = document.getElementById('powerOptions');
        container.innerHTML = '';

        for (const [powerId, powerData] of Object.entries(this.availablePowers)) {
            const button = document.createElement('button');
            button.className = 'shop-item power-item';

            if (this.ownedPowers.has(powerId)) {
                button.classList.add('owned');
                button.innerHTML = `<div>${powerData.name} - OWNED</div><div class="power-desc">${powerData.description}</div>`;
            } else {
                button.innerHTML = `<div>${powerData.name} - ${powerData.price} coins</div><div class="power-desc">${powerData.description}</div>`;
                button.addEventListener('click', () => {
                    if (this.totalCoins >= powerData.price) {
                        this.totalCoins -= powerData.price;
                        this.ownedPowers.add(powerId);
                        this.saveGameData();
                        this.updatePowerShopUI();
                        this.updateUI();
                    }
                });
            }

            container.appendChild(button);
        }
    }

    updateParticleShopUI() {
        const container = document.getElementById('particleOptions');
        container.innerHTML = '';

        for (const [particleId, particleData] of Object.entries(this.availableParticles)) {
            const button = document.createElement('button');
            button.className = 'shop-item';

            if (particleId === this.currentParticle) {
                button.classList.add('selected');
                button.textContent = `${particleData.name} - SELECTED`;
            } else if (this.ownedParticles[particleId]) {
                button.classList.add('owned');
                button.textContent = `${particleData.name} - OWNED`;
                button.addEventListener('click', () => {
                    this.currentParticle = particleId;
                    this.saveGameData();
                    this.updateParticleShopUI();
                    this.updateUI();
                });
            } else {
                button.textContent = `${particleData.name} - ${particleData.price} coins`;
                button.addEventListener('click', () => {
                    if (this.totalCoins >= particleData.price) {
                        this.totalCoins -= particleData.price;
                        this.ownedParticles[particleId] = true;
                        this.currentParticle = particleId;
                        this.saveGameData();
                        this.updateParticleShopUI();
                        this.updateUI();
                    }
                });
            }

            container.appendChild(button);
        }
    }

    updateMusicShopUI() {
        const container = document.getElementById('musicOptions');
        container.innerHTML = '';

        for (const [musicId, musicData] of Object.entries(this.availableMusic)) {
            const button = document.createElement('button');
            button.className = 'shop-item music-item';

            if (musicId === this.currentMusic) {
                button.classList.add('selected');
                button.innerHTML = `<div>${musicData.name} - SELECTED</div>`;
                if (musicData.description) {
                    button.innerHTML += `<div class="music-controls">${musicData.description}</div>`;
                }
                if (musicId !== 'none') {
                    button.innerHTML += `<div class="music-controls">🎵 Currently Playing</div>`;
                }
            } else if (this.ownedMusic[musicId]) {
                button.classList.add('owned');
                button.innerHTML = `<div>${musicData.name} - OWNED</div>`;
                if (musicData.description) {
                    button.innerHTML += `<div class="music-controls">${musicData.description}</div>`;
                }
                if (musicId !== 'none') {
                    button.innerHTML += `<div class="music-controls">▶️ Click to Play</div>`;
                }
                button.addEventListener('click', () => {
                    this.switchMusic(musicId);
                    this.updateMusicShopUI();
                    this.updateUI();
                });
            } else {
                button.innerHTML = `<div>${musicData.name} - ${musicData.price} coins</div>`;
                if (musicData.description) {
                    button.innerHTML += `<div class="music-controls">${musicData.description}</div>`;
                }
                if (musicId !== 'none') {
                    button.innerHTML += `<div class="music-controls">🎶 Click to Preview</div>`;
                }
                button.addEventListener('click', () => {
                    if (this.totalCoins >= musicData.price) {
                        this.totalCoins -= musicData.price;
                        this.ownedMusic[musicId] = true;
                        this.switchMusic(musicId);
                        this.saveGameData();
                        this.updateMusicShopUI();
                        this.updateUI();
                    }
                });
            }

            container.appendChild(button);
        }
    }

    updateUI() {
        // Update coin displays
        document.querySelectorAll('[id$="Coins"]').forEach(el => {
            el.textContent = this.totalCoins;
        });

        // Update high scores
        document.querySelectorAll('.high-score').forEach(el => {
            const diff = el.dataset.difficulty;
            el.textContent = this.highScore[diff] || 0;
        });

        // Update current particle display
        const currentParticleEl = document.getElementById('currentParticle');
        if (currentParticleEl) {
            currentParticleEl.textContent = this.availableParticles[this.currentParticle]?.name || 'None';
        }

        // Update current music display
        const currentMusicEl = document.getElementById('currentMusicTrack');
        if (currentMusicEl) {
            currentMusicEl.textContent = this.availableMusic[this.currentMusic]?.name || 'Original Theme';
        }

        // Update game UI
        if (this.state === GameState.PLAYING) {
            document.getElementById('currentScore').textContent = this.score;
            document.getElementById('currentCoins').textContent = this.score;
            document.getElementById('currentHighScore').textContent = this.highScore[this.difficulty.name] || 0;

            // Update power bars
            this.updatePowerBars();

            // Update shield indicator
            const shieldEl = document.getElementById('shieldIndicator');
            if (this.shieldActive) {
                shieldEl.textContent = `SHIELD: ${this.shieldTimer.toFixed(1)}s`;
                shieldEl.style.display = 'block';
            } else {
                shieldEl.style.display = 'none';
            }
        }

        // Update game over screen
        if (this.state === GameState.GAME_OVER) {
            document.getElementById('coinsEarned').textContent = this.score;
            document.getElementById('finalScore').textContent = this.score;
            document.getElementById('finalHighScore').textContent = Math.max(this.score, this.highScore[this.difficulty.name] || 0);
        }
    }

    updatePowerBars() {
        const container = document.getElementById('powerBars');
        container.innerHTML = '';

        let powerCount = 0;
        for (const powerId of this.ownedPowers) {
            const powerData = this.availablePowers[powerId];
            if (!powerData) continue;

            const barContainer = document.createElement('div');
            barContainer.className = 'power-bar-container';

            const label = document.createElement('div');
            label.className = 'power-label';
            label.textContent = powerId === 'pipe_destroyer' ? 'X:' : 'Z:';

            const bar = document.createElement('div');
            bar.className = 'power-bar';

            const fill = document.createElement('div');
            fill.className = 'power-bar-fill';

            const status = document.createElement('div');
            status.className = 'power-status';

            if (this.powerCooldowns[powerId]) {
                const remaining = this.powerCooldowns[powerId];
                const total = powerData.cooldown;
                const progress = 1 - (remaining / total);
                fill.style.width = `${progress * 100}%`;
                fill.style.backgroundColor = '#FFA500';
                status.textContent = `${remaining.toFixed(1)}s`;
            } else {
                fill.style.width = '100%';
                fill.style.backgroundColor = '#00FF00';
                status.textContent = 'READY';
            }

            bar.appendChild(fill);
            barContainer.appendChild(label);
            barContainer.appendChild(bar);
            barContainer.appendChild(status);
            container.appendChild(barContainer);

            powerCount++;
        }
    }

    resetGame(keepDifficulty = false) {
        // Update high score and add coins before resetting
        if (this.state === GameState.GAME_OVER) {
            this.totalCoins += this.score;

            if (this.score > (this.highScore[this.difficulty.name] || 0)) {
                this.highScore[this.difficulty.name] = this.score;
            }

            this.saveGameData();
        }

        this.bird = new Bird(50, SCREEN_HEIGHT / 2);
        this.pipes = [];
        this.particles = [];

        // Create initial pipes
        for (let i = 0; i < 3; i++) {
            const pipe = new Pipe(SCREEN_WIDTH + i * PIPE_SPACING, this.difficulty);
            this.pipes.push(pipe);
        }

        this.score = 0;
        this.powerCooldowns = {};
        this.shieldActive = false;
        this.shieldTimer = 0;

        // On mobile, try to start music when starting gameplay
        if (keepDifficulty && this.isMobile()) {
            this.tryPlayBackgroundMusic();
        }

        this.setState(keepDifficulty ? GameState.PLAYING : GameState.HOME);
    }

    checkCollision(rect1, rect2) {
        return rect1.x < rect2.x + rect2.width &&
               rect1.x + rect1.width > rect2.x &&
               rect1.y < rect2.y + rect2.height &&
               rect1.y + rect1.height > rect2.y;
    }

    update() {
        if (this.state === GameState.HOME) {
            // Update clouds
            this.clouds.forEach(cloud => cloud.update(this.deltaTime));

            // Remove clouds that have moved off screen and add new ones
            this.clouds = this.clouds.filter(cloud => cloud.x < SCREEN_WIDTH + 100);
            while (this.clouds.length < 5) {
                const cloud = new Cloud();
                cloud.x = -100;
                this.clouds.push(cloud);
            }
            return;
        }

        if (this.state !== GameState.PLAYING) return;

        this.bird.update(this.deltaTime);

        // Update particles
        this.particles = this.particles.filter(particle => particle.update(this.deltaTime));

        // Update power cooldowns
        for (const powerId in this.powerCooldowns) {
            this.powerCooldowns[powerId] -= this.deltaTime;
            if (this.powerCooldowns[powerId] <= 0) {
                delete this.powerCooldowns[powerId];
            }
        }

        // Update shield
        if (this.shieldActive) {
            this.shieldTimer -= this.deltaTime;
            if (this.shieldTimer <= 0) {
                this.shieldActive = false;
            }
        }

        // Update pipes and check for score
        for (const pipe of this.pipes) {
            pipe.update(this.deltaTime);
            if (!pipe.passed && pipe.x < this.bird.x) {
                pipe.passed = true;
                this.score++;
            }
        }

        // Remove off-screen pipes and add new ones
        this.pipes = this.pipes.filter(pipe => pipe.x > -60);
        while (this.pipes.length < 3) {
            const lastPipe = this.pipes.length > 0 ? Math.max(...this.pipes.map(p => p.x)) : SCREEN_WIDTH;
            const newPipe = new Pipe(lastPipe + PIPE_SPACING, this.difficulty);
            this.pipes.push(newPipe);
        }

        // Check for collisions (unless shield is active)
        if (!this.shieldActive) {
            const birdRect = this.bird.getRect();

            // Check boundaries
            if (this.bird.y < 0 || this.bird.y > SCREEN_HEIGHT - this.bird.height) {
                this.setState(GameState.GAME_OVER);
                return;
            }

            // Check pipe collisions
            for (const pipe of this.pipes) {
                if (this.checkCollision(birdRect, pipe.getTopRect()) ||
                    this.checkCollision(birdRect, pipe.getBottomRect())) {
                    this.setState(GameState.GAME_OVER);
                    return;
                }
            }
        }

        this.updateUI();
    }

    draw() {
        // Clear canvas
        this.ctx.clearRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);

        // Draw background
        if (this.assetsLoaded && this.assetLoader.assets.backgroundImage && this.currentBackground === 'default') {
            this.ctx.drawImage(this.assetLoader.assets.backgroundImage, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
        } else {
            // Use background colors for different themes
            const bgColor = this.availableBackgrounds[this.currentBackground]?.color || 'rgb(135, 206, 235)';
            this.ctx.fillStyle = bgColor;
            this.ctx.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);

            // Add ground for non-default backgrounds
            if (this.currentBackground !== 'default') {
                this.ctx.fillStyle = '#DEB887'; // Sandy brown ground
                this.ctx.fillRect(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50);
            }
        }

        if (this.state === GameState.HOME) {
            // Draw clouds
            this.clouds.forEach(cloud => cloud.draw(this.ctx));
            return;
        }

        if (this.state === GameState.PLAYING || this.state === GameState.GAME_OVER) {
            // Draw pipes
            this.pipes.forEach(pipe => pipe.draw(this.ctx, this.assetLoader.assets));

            // Draw particles
            this.particles.forEach(particle => particle.draw(this.ctx));

            // Draw bird
            this.bird.draw(this.ctx, this.currentSkin, this.assetLoader.assets);
        }
    }

    gameLoop(currentTime = 0) {
        // Simple approach: just use fixed delta time for now
        this.deltaTime = 1/60;

        if (!this.assetsLoaded) {
            // Show loading screen
            this.ctx.fillStyle = '#87CEEB';
            this.ctx.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
            this.ctx.fillStyle = '#000';
            this.ctx.font = '16px monospace';
            this.ctx.textAlign = 'center';
            this.ctx.fillText('Loading Assets...', SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2);
            this.ctx.fillText('Please wait', SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 30);
        } else {
            this.update();
            this.draw();
        }

        requestAnimationFrame((time) => this.gameLoop(time));
    }
}

// Start the game when page loads
window.addEventListener('load', () => {
    new Game();
});