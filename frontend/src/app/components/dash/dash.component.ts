import { Component, OnInit, ViewChild } from '@angular/core';

import { StageService } from '../../services/stage.service';
import { GithubService } from '../../services/github.service';
import { NavBarComponent } from '../nav/nav-bar.component';

import { StageCardComponent } from './card/stage-card.component';
import { StageInfoComponent } from '../modals/stage-info.component';
import { StageNewComponent } from '../modals/stage-new.component';

import { Stage } from '../../models/stage';
import { Compare } from '../../models/repo';

@Component({
  selector: 'dashboard',
  templateUrl: 'dash.component.html',
  styleUrls: ['dash.component.scss']
})
export class DashComponent implements OnInit {
  @ViewChild('stageInfoModal') stageInfoModal: StageInfoComponent;
  @ViewChild('stageNewModal') stageNewModal: StageNewComponent;
  private stages: Stage[];
  private autoFetchTimer: any;

  constructor(
    private stageService: StageService,
    private githubService: GithubService
  ) {}

  ngOnInit() {
    this.fetchStages();
    this.autoFetchTimer = setInterval(() => { this.fetchStages(); }, 2000);
  }

  ngOnDestroy() {
    if (this.autoFetchTimer) {
      clearInterval(this.autoFetchTimer);
    }
  }

  private fetchCommitDiff(stages: Stage[]) {
    let promises: Promise<Stage>[] = [];
    for (let stage of stages) {
      let promise = this.githubService.getCompareBranch(stage).then((compare: Compare) => {
        stage.compare_url = compare.permalink_url;
        stage.commits = compare.commits;
        return stage;
      });
      promises.push(promise);
    };
    return Promise.all(promises);
  }

  private fetchStages() {
    this.stageService.getStages().then((stages: Stage[]) => {
      this.fetchCommitDiff(stages).then((stagesWithDiff: Stage[]) => {
        this.stages = stagesWithDiff;
      });
    });
  }

  private onShowStageInfo(event: any) {
    this.stageInfoModal.showModal(event.value);
  }

  private onToggleStageStatus(event: any) {
    let targetStage: Stage = event.value;
    this.stageService.toggleStatus(targetStage).then(() => {
      targetStage.status = 'changing';
    });
  }

  private onAddNewStage(event: any) {
    this.stageNewModal.showModal();
  }

  private onCreateNewStage(event: any) {
    let newStageInfo = event.value;
    let runOnClose = newStageInfo.runOnClose;

    this.stageService.createStage(newStageInfo).then((stage: Stage) => {
      this.fetchStages();
    })
  }

  private onTrashStage(event: any) {
    let targetStage: Stage = event.value;
    this.stageService.deleteStage(targetStage).then(() => {
      targetStage.status = 'deleting';
    })
  }

  private onRefreshStage(event: any) {
    let targetStage: Stage = event.value;
    this.stageService.refreshStage(targetStage).then(() => {
      targetStage.status = 'changing';
    })
  }
}