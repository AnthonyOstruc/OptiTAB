import Phaser from 'phaser'
import { getRandomQuestion } from '../data/questions.js'
import { sfx } from '../audio.js'

const HUD_H    = 60
const Q_H      = 82
const GAME_TOP = 142
const HORIZON_Y = 162
const H_ROAD_HALF  = 54
const H_DIV_OFFSET = 18
const H_LANE_CX = [204, 240, 276]
const PLAYER_OFFSET = 138
const MOBILE_BTN_Y_OFFSET = 52
const STRIPE_SPACING = 82

const CAT_ACCENT = {
  addition:0x22c55e, subtraction:0xf59e0b, multiplication:0xa78bfa,
  division:0x22d3ee, limits:0xa855f7, derivatives:0x818cf8,
  integrals:0x34d399, sequences:0xfb923c, all:0x3b82f6,
}
const CAT_COLOR_HEX = {
  addition:'#4ade80', subtraction:'#fbbf24', multiplication:'#c4b5fd',
  division:'#67e8f9', limits:'#d8b4fe', derivatives:'#a5b4fc',
  integrals:'#6ee7b7', sequences:'#fdba74', all:'#93c5fd',
}
const CAT_ICON = {
  addition:'+', subtraction:'−', multiplication:'×', division:'÷',
  limits:'lim', derivatives:'d/dx', integrals:'∫', sequences:'uₙ', all:'∞',
}

const SPEED_TIERS = [
  [0,5800,65],[5,5200,95],[10,4700,130],[15,4200,170],[20,3800,215],
]

function clamp(v,lo,hi){ return v<lo?lo:v>hi?hi:v }

export default class GameScene extends Phaser.Scene {
  constructor(){ super({ key:'GameScene' }) }

  init(data){
    this.score=0; this.lives=3; this.currentLane=1
    this.isEvaluating=false; this.answerBlocks=[]; this.blockTweens=[]
    this.playerPos={x:0}; this.currentTier=0; this.runTick=0
    this.streak=0; this.timerElapsed=0; this.questionDuration=0
    this.stripeOffset=0; this.stripeSpeed=65
    this.category = data?.category || 'all'
  }

  _laneXatY(laneIdx, y){
    const t = clamp((y - HORIZON_Y)/(this.H - HORIZON_Y), 0, 1)
    return H_LANE_CX[laneIdx] + t*(this.laneX[laneIdx] - H_LANE_CX[laneIdx])
  }
  _perspScale(y){
    const t = clamp((y - HORIZON_Y)/(this.H - HORIZON_Y), 0, 1)
    return 0.18 + t*0.82
  }

  create(){
    const W=this.scale.width, H=this.scale.height
    this.W=W; this.H=H
    this.laneW = W/3
    this.laneX = [W/6, W/2, (5*W)/6]
    this.playerY    = H - PLAYER_OFFSET
    this.blockStartY = HORIZON_Y + 20
    this.blockTargetY = this.playerY - 40
    this.playerPos.x  = this._laneXatY(1, this.playerY)
    this.accentColor  = CAT_ACCENT[this.category] || 0x3b82f6

    this._buildWorld()
    this._buildHUD()
    this._buildQuestionPanel()
    this._buildPlayer()
    this._buildMobileControls()
    this._bindKeys()

    this.input.keyboard.on('keydown-ESC', ()=>{
      this.cameras.main.fadeOut(200,4,13,26)
      this.time.delayedCall(200,()=>this.scene.start('MenuScene'))
    })
    this._startCountdown()
  }

  _buildWorld(){
    const W=this.W, H=this.H
    this.add.rectangle(W/2, GAME_TOP+(HORIZON_Y-GAME_TOP)/2, W, HORIZON_Y-GAME_TOP+2, 0x030810)
    this._buildCity()

    const atmGfx = this.add.graphics()
    atmGfx.fillStyle(this.accentColor, 0.1)
    atmGfx.fillRect(0, HORIZON_Y-12, W, 12)

    const road = this.add.graphics()
    road.fillStyle(0x060d1e, 1)
    road.fillPoints([
      {x:W/2-H_ROAD_HALF,y:HORIZON_Y},{x:W/2+H_ROAD_HALF,y:HORIZON_Y},
      {x:W,y:H},{x:0,y:H},
    ], true)
    road.fillStyle(0x030810, 0.3)
    road.fillPoints([
      {x:W/2-H_ROAD_HALF,y:HORIZON_Y},{x:W/2-H_DIV_OFFSET,y:HORIZON_Y},
      {x:this.laneX[0]+this.laneW/2,y:H},{x:0,y:H},
    ], true)
    road.fillStyle(0x030810, 0.3)
    road.fillPoints([
      {x:W/2+H_DIV_OFFSET,y:HORIZON_Y},{x:W/2+H_ROAD_HALF,y:HORIZON_Y},
      {x:W,y:H},{x:this.laneX[1]+this.laneW/2,y:H},
    ], true)
    road.fillStyle(0x0f1e3a, 0.15)
    road.fillPoints([
      {x:W/2-H_DIV_OFFSET,y:HORIZON_Y},{x:W/2+H_DIV_OFFSET,y:HORIZON_Y},
      {x:this.laneX[1]+this.laneW/2,y:H},{x:this.laneX[0]+this.laneW/2,y:H},
    ], true)

    this._buildDividers()

    this.stripeGfx = this.add.graphics().setDepth(5)
    this.stripeRows = []
    const total = Math.ceil((H - HORIZON_Y)/STRIPE_SPACING) + 2
    for(let lane=0;lane<3;lane++){
      for(let row=0;row<total;row++){
        this.stripeRows.push({ lane, baseOffset: row*STRIPE_SPACING })
      }
    }
  }

  _buildCity(){
    const W=this.W
    const g = this.add.graphics()
    const BOT = HORIZON_Y - 1
    const bldgs = [
      {x:6,  w:32,h:56, win:[[6,14],[6,30],[18,14],[18,30]]},
      {x:42, w:42,h:80, win:[[6,12],[6,30],[6,50],[24,12],[24,30]]},
      {x:90, w:28,h:40, win:[[6,14],[16,14]]},
      {x:124,w:36,h:66, win:[[6,14],[6,32],[20,14],[20,32]]},
      {x:162,w:22,h:34, win:[[6,12]]},
      {x:296,w:24,h:38, win:[[5,12],[13,12]]},
      {x:324,w:38,h:70, win:[[6,14],[6,32],[22,14],[22,32]]},
      {x:366,w:28,h:44, win:[[6,14],[16,14]]},
      {x:398,w:44,h:86, win:[[6,12],[6,30],[6,50],[26,12],[26,30]]},
      {x:446,w:32,h:58, win:[[6,14],[18,14],[6,30]]},
    ]
    bldgs.forEach(({x,w,h,win})=>{
      g.fillStyle(0x050b1a,1)
      g.fillRect(x, BOT-h, w, h)
      g.fillStyle(this.accentColor, 0.07)
      g.fillRect(x, BOT-h, w, 2)
      win.forEach(([wx,wy])=>{
        if(Math.random()>0.28){
          g.fillStyle(0xfbbf24, 0.5+Math.random()*0.3)
          g.fillRect(x+wx, BOT-h+wy, 5, 6)
        }
      })
    })
    g.fillStyle(0x1e3a8a, 0.1)
    g.fillRect(0, BOT-6, W, 6)
  }

  _buildDividers(){
    const W=this.W, H=this.H
    const lDtx=W/2-H_DIV_OFFSET, lDbx=this.laneW
    const rDtx=W/2+H_DIV_OFFSET, rDbx=this.laneW*2
    const eLtx=W/2-H_ROAD_HALF, eRtx=W/2+H_ROAD_HALF
    const dg = this.add.graphics().setDepth(6);
    [[20,0.03],[10,0.08],[4,0.28],[1.5,0.85]].forEach(([lw,a],i)=>{
      const col = i<3 ? 0x3b82f6 : 0x93c5fd
      dg.lineStyle(lw,col,a)
      dg.lineBetween(lDtx,HORIZON_Y,lDbx,H)
      dg.lineBetween(rDtx,HORIZON_Y,rDbx,H)
    })
    dg.lineStyle(8,this.accentColor,0.05)
    dg.lineBetween(eLtx,HORIZON_Y,0,H)
    dg.lineBetween(eRtx,HORIZON_Y,W,H)
    dg.lineStyle(1.5,this.accentColor,0.2)
    dg.lineBetween(eLtx,HORIZON_Y,0,H)
    dg.lineBetween(eRtx,HORIZON_Y,W,H)
  }

  _drawStripes(){
    const gfx=this.stripeGfx
    gfx.clear()
    const range=this.H-HORIZON_Y
    this.stripeRows.forEach(({lane,baseOffset})=>{
      const rawY=HORIZON_Y+(baseOffset+this.stripeOffset)%range
      if(rawY<HORIZON_Y+5) return
      const t=clamp((rawY-HORIZON_Y)/range,0,1)
      const x=this._laneXatY(lane,rawY)
      const w=4+t*44, h=2+t*8
      gfx.fillStyle(0xffffff,0.04+t*0.04)
      gfx.fillRoundedRect(x-w/2,rawY-h/2,w,h,2)
    })
  }

  _buildHUD(){
    const W=this.W
    this.add.rectangle(W/2,HUD_H/2,W,HUD_H,0x020810).setDepth(10)
    this.add.rectangle(W/2,HUD_H,W,1,0x1e3a8a,0.5).setDepth(10)

    this.add.text(14,10,'SCORE',{fontSize:'9px',fontFamily:"'Segoe UI',Arial,sans-serif",color:'#1e3a8a',fontStyle:'bold',letterSpacing:1}).setDepth(11)
    this.scoreTxt=this.add.text(14,22,'0',{fontSize:'26px',fontFamily:"'Segoe UI',Arial,sans-serif",color:'#e2e8f0',fontStyle:'bold'}).setDepth(11)
    this.streakTxt=this.add.text(14,52,'',{fontSize:'11px',fontFamily:"'Segoe UI',Arial,sans-serif",color:'#fbbf24',fontStyle:'bold'}).setDepth(11).setAlpha(0)

    const halo=this.add.graphics().setDepth(10)
    halo.fillStyle(this.accentColor,0.18); halo.fillCircle(W/2,HUD_H/2,22)
    const icon=CAT_ICON[this.category]||'∞'
    this.add.text(W/2,HUD_H/2,icon,{fontSize:icon.length>2?'12px':'21px',fontFamily:'Arial',color:CAT_COLOR_HEX[this.category]||'#93c5fd',fontStyle:'bold'}).setOrigin(0.5).setDepth(11)

    this.add.text(W-14,10,'VIES',{fontSize:'9px',fontFamily:"'Segoe UI',Arial,sans-serif",color:'#1e3a8a',fontStyle:'bold',letterSpacing:1}).setOrigin(1,0).setDepth(11)
    this.livesTxt=this.add.text(W-14,22,'♥  ♥  ♥',{fontSize:'18px',fontFamily:"'Segoe UI',Arial,sans-serif",color:'#ff5252'}).setOrigin(1,0).setDepth(11)
  }

  _buildQuestionPanel(){
    const W=this.W, panelY=HUD_H+Q_H/2
    this.add.rectangle(W/2,panelY,W,Q_H,0x060d1e).setDepth(10)
    this.add.rectangle(3,panelY,6,Q_H,this.accentColor,0.9).setDepth(11)
    this.add.rectangle(W/2,HUD_H+0.5,W,1,0x1e3a8a,0.6).setDepth(11)
    this.add.rectangle(W/2,HUD_H+Q_H-0.5,W,1,this.accentColor,0.3).setDepth(11)
    const catName={addition:'Addition',subtraction:'Soustraction',multiplication:'Multiplication',division:'Division',limits:'Limites',derivatives:'Dérivées',integrals:'Intégrales',sequences:'Suites',all:'Mixte'}[this.category]||'Mixte'
    this.add.text(W-10,HUD_H+9,catName,{fontSize:'9px',fontFamily:"'Segoe UI',Arial,sans-serif",color:CAT_COLOR_HEX[this.category]||'#475569',fontStyle:'bold'}).setOrigin(1,0).setDepth(11)
    this.questionTxt=this.add.text(W/2,panelY,'',{fontSize:'26px',fontFamily:"'Segoe UI',Arial,sans-serif",color:'#ffffff',fontStyle:'bold'}).setOrigin(0.5).setDepth(11)
    this.add.rectangle(W/2,HUD_H+Q_H-4,W,8,0x020810).setDepth(10)
    this.timerBarGfx=this.add.graphics().setDepth(11)
  }

  _buildPlayer(){
    this.playerGlowGfx=this.add.graphics().setDepth(13)
    this.playerGfx=this.add.graphics().setDepth(15)
    this._drawPlayer()
    this.laneBar=this.add.rectangle(this._laneXatY(1,this.playerY+50),this.playerY+50,this.laneW-24,4,this.accentColor).setAlpha(0.5).setDepth(14)
  }

  _drawPlayer(){
    const glow=this.playerGlowGfx; glow.clear()
    glow.fillStyle(this.accentColor,0.1); glow.fillEllipse(this.playerPos.x,this.playerY+54,88,20)
    glow.fillStyle(this.accentColor,0.05); glow.fillEllipse(this.playerPos.x,this.playerY+54,130,32)

    const g=this.playerGfx; g.clear()
    const x=this.playerPos.x, y=this.playerY
    const t=this.runTick*Math.PI*2
    const bob=Math.abs(Math.sin(t*2))*3
    const leg=Math.sin(t), arm=Math.sin(t+Math.PI)
    const SKIN=0xf5c5a3,HAIR=0x2d1b0e,SHIRT=0x2563eb,NAVY=0x1e3a8a,SHOE=0x1c1c2e,SOLE=0xdddddd
    const by=-bob
    const rLeg=-leg,rShoe=x-15+rLeg*7
    g.fillStyle(NAVY,1); g.fillRoundedRect(x-15,y+15+by+rLeg*3,12,14,4)
    g.fillStyle(SKIN,1); g.fillRoundedRect(x-15+rLeg*4,y+27+by+rLeg*3,11,13,3)
    g.fillStyle(SHOE,1); g.fillRoundedRect(rShoe-1,y+38+by,17,8,4)
    g.fillStyle(SOLE,1); g.fillRect(rShoe-1,y+44+by,17,2)
    g.fillStyle(SHIRT,1); g.fillRoundedRect(x-22,y-16+by+arm*6,8,13,4)
    g.fillStyle(SKIN,1);  g.fillRoundedRect(x-21,y-5+by+arm*9,7,10,3)
    g.fillStyle(SHIRT,1); g.fillRoundedRect(x-14,y-22+by,28,30,6)
    g.fillStyle(0x60a5fa,1); g.fillRoundedRect(x-2,y-22+by,4,11,2)
    g.fillStyle(NAVY,1); g.fillRoundedRect(x-14,y+6+by,28,11,4)
    const fShoe=x+3+leg*7
    g.fillStyle(NAVY,1); g.fillRoundedRect(x+3,y+15+by+leg*3,12,14,4)
    g.fillStyle(SKIN,1); g.fillRoundedRect(x+4+leg*4,y+27+by+leg*3,11,13,3)
    g.fillStyle(SHOE,1); g.fillRoundedRect(fShoe-1,y+38+by,17,8,4)
    g.fillStyle(SOLE,1); g.fillRect(fShoe-1,y+44+by,17,2)
    g.fillStyle(SHIRT,1); g.fillRoundedRect(x+14,y-16+by-arm*6,8,13,4)
    g.fillStyle(SKIN,1);  g.fillRoundedRect(x+14,y-5+by-arm*9,7,10,3)
    g.fillStyle(SKIN,1); g.fillRoundedRect(x-5,y-25+by,10,7,3); g.fillEllipse(x,y-37+by,26,28)
    g.fillStyle(HAIR,1); g.fillEllipse(x,y-47+by,28,14); g.fillRoundedRect(x-14,y-50+by,5,12,2); g.fillRoundedRect(x+9,y-50+by,5,12,2)
    g.fillStyle(0xffffff,1); g.fillEllipse(x-6,y-38+by,9,8); g.fillEllipse(x+6,y-38+by,9,8)
    g.fillStyle(0x1a237e,1); g.fillCircle(x-6,y-38+by,3); g.fillCircle(x+6,y-38+by,3)
    g.fillStyle(0xffffff,1); g.fillCircle(x-5,y-39+by,1.2); g.fillCircle(x+7,y-39+by,1.2)
    g.fillStyle(HAIR,1); g.fillRoundedRect(x-9,y-44+by,7,2,1); g.fillRoundedRect(x+2,y-44+by,7,2,1)
    g.fillStyle(0xd4956a,1); g.fillRoundedRect(x-4,y-31+by,8,2.5,1)
  }

  _buildMobileControls(){
    const y=this.H-MOBILE_BTN_Y_OFFSET
    this._makeBtn(this.W*0.09,y,84,54,'◀',()=>this._moveLeft())
    this._makeBtn(this.W/2,   y,60,54,'≡',()=>{
      this.cameras.main.fadeOut(200,4,13,26)
      this.time.delayedCall(200,()=>this.scene.start('MenuScene'))
    })
    this._makeBtn(this.W*0.91,y,84,54,'▶',()=>this._moveRight())
  }
  _makeBtn(x,y,w,h,label,cb){
    const bg=this.add.graphics().setDepth(20)
    const draw=(p)=>{
      bg.clear(); bg.fillStyle(p?0x1e3a8a:0x060d1e,p?1:0.88)
      bg.fillRoundedRect(x-w/2,y-h/2,w,h,12)
      bg.lineStyle(1.5,p?0x60a5fa:0x1e3a8a,0.7); bg.strokeRoundedRect(x-w/2,y-h/2,w,h,12)
    }
    draw(false)
    const btn=this.add.text(x,y,label,{fontSize:'26px',fontFamily:'Arial',color:'#60a5fa'}).setOrigin(0.5).setDepth(21).setInteractive({useHandCursor:true})
    btn.on('pointerdown',()=>{ draw(true); cb() }); btn.on('pointerup',()=>draw(false)); btn.on('pointerout',()=>draw(false))
  }

  _bindKeys(){
    this.input.keyboard.on('keydown-LEFT', ()=>this._moveLeft())
    this.input.keyboard.on('keydown-RIGHT',()=>this._moveRight())
    this.input.keyboard.on('keydown-A',    ()=>this._moveLeft())
    this.input.keyboard.on('keydown-D',    ()=>this._moveRight())
  }
  _moveLeft(){  if(this.isEvaluating||this.currentLane<=0) return; this.currentLane--; sfx.laneSwitch(); this._animatePlayerToLane() }
  _moveRight(){ if(this.isEvaluating||this.currentLane>=2) return; this.currentLane++; sfx.laneSwitch(); this._animatePlayerToLane() }
  _animatePlayerToLane(){
    const tx=this._laneXatY(this.currentLane,this.playerY)
    const bx=this._laneXatY(this.currentLane,this.playerY+50)
    this.tweens.killTweensOf(this.playerPos)
    this.tweens.add({targets:this.playerPos,x:tx,duration:130,ease:'Power2'})
    this.tweens.add({targets:this.laneBar,  x:bx,duration:130,ease:'Power2'})
  }

  _getTier(){ for(let i=SPEED_TIERS.length-1;i>=0;i--){ if(this.score>=SPEED_TIERS[i][0]) return i } return 0 }
  _getFallDuration(){ return SPEED_TIERS[this._getTier()][1] }
  _updateSpeed(){
    const tier=this._getTier(); if(tier<=this.currentTier) return
    this.currentTier=tier; this.stripeSpeed=SPEED_TIERS[tier][2]; sfx.speedUp(); this._showSpeedUp()
  }
  _showSpeedUp(){
    const msg=this.add.text(this.W/2,this.H*0.36,'⚡  VITESSE +',{fontSize:'22px',fontFamily:"'Segoe UI',Arial,sans-serif",color:'#fbbf24',fontStyle:'bold',stroke:'#000c1a',strokeThickness:4}).setOrigin(0.5).setAlpha(0).setDepth(22)
    this.tweens.add({targets:msg,alpha:1,y:this.H*0.29,duration:280,hold:700,yoyo:true,onComplete:()=>msg.destroy()})
  }

  _nextQuestion(){
    if(this.isEvaluating) return
    this._updateSpeed()
    const q=getRandomQuestion(this.category)
    this.currentQuestion=q
    this.questionTxt.setAlpha(0).setText(q.question)
    this.tweens.add({targets:this.questionTxt,alpha:1,duration:200})
    this.timerElapsed=0
    this._spawnBlocks(q)
  }

  _spawnBlocks(q){
    this._clearBlocks()
    const bW=this.laneW-22, bH=60
    const fallDuration=this._getFallDuration()
    for(let i=0;i<3;i++){
      const startX=this._laneXatY(i,this.blockStartY)
      const container=this.add.container(startX,this.blockStartY).setDepth(12)
      container.setScale(this._perspScale(this.blockStartY))
      const bg=this.add.graphics()
      bg.fillStyle(0x060d1e,1); bg.fillRoundedRect(-bW/2,-bH/2,bW,bH,10)
      bg.lineStyle(16,this.accentColor,0.05); bg.strokeRoundedRect(-bW/2,-bH/2,bW,bH,10)
      bg.lineStyle(7,this.accentColor,0.12);  bg.strokeRoundedRect(-bW/2,-bH/2,bW,bH,10)
      bg.lineStyle(2,this.accentColor,0.7);   bg.strokeRoundedRect(-bW/2,-bH/2,bW,bH,10)
      bg.fillStyle(0xffffff,0.07); bg.fillRoundedRect(-bW/2+3,-bH/2+3,bW-6,bH*0.35,7)
      bg.lineStyle(2,this.accentColor,0.35); bg.lineBetween(-bW/2+12,bH/2-1,bW/2-12,bH/2-1)
      const txt=this.add.text(0,0,String(q.answers[i]),{fontSize:'24px',fontFamily:"'Segoe UI',Arial,sans-serif",color:'#e2e8f0',fontStyle:'bold'}).setOrigin(0.5)
      container.add([bg,txt])
      const tween=this.tweens.add({
        targets:container, y:this.blockTargetY, duration:fallDuration, ease:'Linear',
        onUpdate:()=>{
          container.setScale(this._perspScale(container.y))
          container.x=this._laneXatY(i,container.y)
        },
        onComplete:()=>{ if(!this.isEvaluating) this._evaluate() },
      })
      this.questionDuration=fallDuration
      this.answerBlocks.push({container,answer:q.answers[i]})
      this.blockTweens.push(tween)
    }
  }

  _clearBlocks(){
    this.blockTweens.forEach(t=>{if(t?.isPlaying?.()) t.stop()})
    this.answerBlocks.forEach(b=>b.container?.destroy())
    this.answerBlocks=[]; this.blockTweens=[]
  }

  _evaluate(){
    if(this.isEvaluating) return
    this.isEvaluating=true; this.questionDuration=0; this.timerBarGfx.clear()
    this.blockTweens.forEach(t=>{if(t?.isPlaying?.()) t.stop()})
    const sel=this.answerBlocks[this.currentLane]
    const correct=sel&&String(sel.answer)===String(this.currentQuestion.correctAnswer)
    if(correct){
      this.streak++; const mult=this._getMultiplier()
      this.score+=mult; this.scoreTxt.setText(String(this.score))
      this._updateStreakDisplay(); window.dispatchEvent(new CustomEvent('mathrun:correct'))
      if(this.streak===3||this.streak===5||this.streak===10){
        this.time.delayedCall(200,()=>this._showCombo(this.streak))
        this._emitParticles(this.W/2,this.H*0.5,0xffd54f,26)
      }
      if(mult>1) this._showBonus(mult)
    } else {
      this.streak=0; this._updateStreakDisplay(); this.lives--; this._updateHearts()
    }
    if(correct) sfx.correct(); else if(this.lives<=0) sfx.gameOver(); else sfx.wrong()
    this._showFeedback(correct)
    if(this.lives<=0){
      this.time.delayedCall(1300,()=>this.scene.start('GameOverScene',{score:this.score,category:this.category}))
    } else {
      this.time.delayedCall(1100,()=>{ this._clearBlocks(); this.isEvaluating=false; this._nextQuestion() })
    }
  }

  _emitParticles(cx,cy,color,count=14){
    for(let i=0;i<count;i++){
      const angle=(i/count)*Math.PI*2+Math.random()*0.4
      const speed=55+Math.random()*100
      const dot=this.add.circle(cx,cy,3+Math.random()*5,color).setDepth(25).setAlpha(0.9)
      this.tweens.add({targets:dot,x:cx+Math.cos(angle)*speed,y:cy+Math.sin(angle)*speed-22,alpha:0,scaleX:0.1,scaleY:0.1,delay:Math.random()*60,duration:460+Math.random()*200,ease:'Power2.easeOut',onComplete:()=>dot.destroy()})
    }
  }

  _showFeedback(correct){
    if(correct){ this._emitParticles(this.playerPos.x,this.playerY-22,0x22c55e,20); this._emitParticles(this.playerPos.x,this.playerY-22,0xffd54f,10) }
    const color=correct?0x22c55e:0xef4444
    const W=this.W,H=this.H
    const flash=this.add.rectangle(W/2,H/2,W,H,color,0).setDepth(18)
    this.tweens.add({targets:flash,alpha:correct?0.13:0.22,yoyo:true,duration:240,onComplete:()=>flash.destroy()})
    if(!correct) this.cameras.main.shake(200,0.007)
    const msg=this.add.text(W/2,H/2-50,correct?'✓  Correct !':'✗  Incorrect',{
      fontSize:'36px',fontFamily:"'Segoe UI',Arial,sans-serif",
      color:correct?'#4ade80':'#f87171',fontStyle:'bold',stroke:'#000c1a',strokeThickness:5,
    }).setOrigin(0.5).setAlpha(0).setDepth(19)
    this.tweens.add({targets:msg,alpha:1,y:H/2-80,duration:250,hold:480,yoyo:true,onComplete:()=>msg.destroy()})
    const selB=this.answerBlocks[this.currentLane]
    if(selB){
      const sc=selB.container.scaleX, bW=this.laneW-22
      const hl=this.add.graphics().setDepth(13)
      hl.fillStyle(color,0.38); hl.fillRoundedRect(selB.container.x-bW*sc/2,selB.container.y-30*sc,bW*sc,60*sc,8)
      this.time.delayedCall(900,()=>hl.destroy())
    }
    if(!correct){
      const ci=this.answerBlocks.findIndex(b=>String(b.answer)===String(this.currentQuestion.correctAnswer))
      if(ci!==-1){
        const cb=this.answerBlocks[ci], sc=cb.container.scaleX, cbW=this.laneW-22
        const chl=this.add.graphics().setDepth(13)
        chl.fillStyle(0x22c55e,0.28); chl.fillRoundedRect(cb.container.x-cbW*sc/2,cb.container.y-30*sc,cbW*sc,60*sc,8)
        chl.lineStyle(2,0x22c55e,0.7); chl.strokeRoundedRect(cb.container.x-cbW*sc/2,cb.container.y-30*sc,cbW*sc,60*sc,8)
        this.time.delayedCall(900,()=>chl.destroy())
      }
    }
  }

  _updateHearts(){ this.livesTxt.setText(Array(Math.max(this.lives,0)).fill('♥').join('  ')||'—') }

  _startCountdown(){
    const labels=['3','2','1','GO !'],colors=['#e2e8f0','#e2e8f0','#ffd54f','#4ade80'],sizes=['86px','86px','86px','60px']
    let idx=0
    const tick=()=>{
      if(idx>=labels.length){ this.isEvaluating=false; this._nextQuestion(); return }
      if(idx<3) sfx.laneSwitch(); else sfx.correct()
      const txt=this.add.text(this.W/2,this.H/2,labels[idx],{fontSize:sizes[idx],fontFamily:"'Segoe UI',Arial,sans-serif",color:colors[idx],fontStyle:'bold',stroke:'#000c1a',strokeThickness:7}).setOrigin(0.5).setAlpha(0).setScale(1.7).setDepth(35)
      this.tweens.add({targets:txt,alpha:1,scaleX:1,scaleY:1,duration:170,ease:'Back.easeOut',
        onComplete:()=>this.tweens.add({targets:txt,alpha:0,delay:idx<3?450:300,duration:140,onComplete:()=>{txt.destroy();idx++;tick()}})})
    }
    this.isEvaluating=true; this.time.delayedCall(300,tick)
  }

  _getMultiplier(){ return this.streak>=10?5:this.streak>=5?3:this.streak>=3?2:1 }
  _updateStreakDisplay(){ if(this.streak>=2) this.streakTxt.setText(`🔥 ×${this.streak}`).setAlpha(1); else this.streakTxt.setAlpha(0) }
  _showCombo(n){
    const cols={3:'#fbbf24',5:'#f97316',10:'#ef4444'}
    const msg=this.add.text(this.W/2,this.H*0.44,`COMBO  ×${n} !`,{fontSize:'32px',fontFamily:"'Segoe UI',Arial,sans-serif",color:cols[n]||'#fbbf24',fontStyle:'bold',stroke:'#000c1a',strokeThickness:4}).setOrigin(0.5).setAlpha(0).setDepth(22)
    this.tweens.add({targets:msg,alpha:1,y:this.H*0.37,duration:280,hold:600,yoyo:true,onComplete:()=>msg.destroy()})
  }
  _showBonus(n){
    const b=this.add.text(this.playerPos.x+36,this.playerY-68,`+${n}`,{fontSize:'24px',fontFamily:"'Segoe UI',Arial,sans-serif",color:'#ffd54f',fontStyle:'bold',stroke:'#000c1a',strokeThickness:2}).setOrigin(0.5).setAlpha(0).setDepth(24)
    this.tweens.add({targets:b,alpha:1,y:this.playerY-102,duration:250,hold:360,yoyo:true,onComplete:()=>b.destroy()})
  }

  update(time, delta){
    const dt=delta/1000
    this.stripeOffset=(this.stripeOffset+this.stripeSpeed*dt)%(this.H-HORIZON_Y)
    this._drawStripes()
    this.runTick=(this.runTick+dt/0.32)%1
    this._drawPlayer()
    if(!this.isEvaluating&&this.questionDuration>0){
      this.timerElapsed+=delta
      const ratio=Math.max(0,1-this.timerElapsed/this.questionDuration)
      const barW=ratio*this.W
      const col=ratio>0.5?this.accentColor:ratio>0.25?0xf59e0b:0xef4444
      this.timerBarGfx.clear()
      if(barW>0){ this.timerBarGfx.fillStyle(col,1); this.timerBarGfx.fillRoundedRect(0,HUD_H+Q_H-8,barW,8,{bl:0,br:ratio<0.97?4:0,tl:0,tr:0}) }
    }
  }
}
