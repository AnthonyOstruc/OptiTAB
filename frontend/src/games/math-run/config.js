import Phaser from 'phaser'
import BootScene from './scenes/BootScene.js'
import MenuScene from './scenes/MenuScene.js'
import GameScene from './scenes/GameScene.js'
import GameOverScene from './scenes/GameOverScene.js'

export function createPhaserConfig(parent) {
  return {
    type: Phaser.AUTO,
    parent,
    width: 480,
    height: 700,
    backgroundColor: '#060e1e',
    scene: [BootScene, MenuScene, GameScene, GameOverScene],
    scale: {
      mode: Phaser.Scale.FIT,
      autoCenter: Phaser.Scale.CENTER_BOTH,
    },
    input: {
      activePointers: 3,
    },
  }
}
