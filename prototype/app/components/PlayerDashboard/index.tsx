'use client';

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine, Label } from 'recharts';
import { User } from 'lucide-react';

interface PlayerInfo {
  name: string;
  dateOfBirth: string;
  age: number;
  placeOfBirth: string;
  height: string;
  citizenship: string[];
  position: string;
  foot: string;
  team: string;
  photoUrl?: string;
}

interface CommonStat {
  value: string | number;
  sites: string[];
}

interface UniqueStat {
  stat: string;
  value: string | number;
  source: string;
}

interface SubjectiveMetric {
  metric: string;
  average: number;
  FotMob?: number;
  SofaScore?: number;
  FBref?: number;
  Understat?: number;
  WhoScored?: number;
  [key: string]: string | number | undefined;
}

interface RecentMatch {
  date: string;
  opponent: string;
  result: string;
  minutesPlayed: number;
  goals: number;
  assists: number;
  yellowCards: number;
  redCards: number;
  rating: number;
}

interface PlayerData {
  playerInfo: PlayerInfo;
  commonStats: Record<string, CommonStat>;
  uniqueStats: UniqueStat[];
  subjectiveData: SubjectiveMetric[];
  recentMatches: RecentMatch[];
}

const PlayerDashboard: React.FC<{ data: PlayerData }> = ({ data }) => {
  const getPlayerStatus = (rating: number) => {
    if (rating <= 4.0) {
      return {
        text: '양호',
        color: 'text-green-600',
        bgColor: 'bg-green-100'
      };
    } else if (rating <= 6.5) {
      return {
        text: '주의',
        color: 'text-yellow-600',
        bgColor: 'bg-yellow-100'
      };
    } else {
      return {
        text: '경고',
        color: 'text-red-600',
        bgColor: 'bg-red-100'
      };
    }
  };

  const averageRating = data.subjectiveData.find(data => data.metric === 'Match Rating')?.average || 0;
  const status = getPlayerStatus(averageRating as number);

  const transformMetricData = (metricData: SubjectiveMetric) => {
    const sites = Object.keys(metricData).filter(key => 
      key !== 'metric' && key !== 'average' && metricData[key] !== undefined
    );

    return sites.map(site => ({
      site,
      value: metricData[site] as number
    }));
  };

  return (
<div className="w-full max-w-3xl mx-auto p-4 space-y-4 bg-gray-50">
  {/* Header */}
  <div className="flex items-center space-x-4 bg-white p-6 rounded-lg shadow">
    <div className="w-24 h-24 bg-gray-200 rounded-full flex items-center justify-center">
      {data.playerInfo.photoUrl ? (
        <img 
          src={data.playerInfo.photoUrl} 
          alt={data.playerInfo.name} 
          className="w-full h-full rounded-full object-cover" 
        />
      ) : (
        <User size={48} />
      )}
    </div>
    <div className="flex-grow">
      <h1 className="text-2xl font-bold">{data.playerInfo.name}</h1>
      <div className="space-y-1">
        <p className="text-gray-600">
          {data.playerInfo.team} | {data.playerInfo.position}
        </p>
        <p className="text-sm text-gray-600">
          {data.playerInfo.dateOfBirth} ({data.playerInfo.age}세) | {data.playerInfo.height}
        </p>
        <p className="text-sm text-gray-600">
          출생지: {data.playerInfo.placeOfBirth} | 국적: {data.playerInfo.citizenship.join(', ')} | 주발: {data.playerInfo.foot}
        </p>
      </div>
      <div className="mt-2">
        <span className="text-sm text-gray-500">데이터 출처: WhoScored, FotMob, SofaScore, FBref, Transfermarkt</span>
      </div>
    </div>
    <div className={`px-4 py-2 rounded-lg ${status.bgColor}`}>
      <p className={`text-3xl font-bold ${status.color}`}>{status.text}</p>
      <p className="text-sm text-gray-600">평균 평점: {(averageRating as number).toFixed(2)}</p>
    </div>
  </div>

      {/* Common Stats */}
      <Card>
        <CardHeader>
          <CardTitle>객관적 지표 (전체 사이트 공통)</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {Object.entries(data.commonStats).map(([key, data]) => (
              <div key={key} className="p-4 bg-gray-50 rounded">
                <p className="text-sm text-gray-600">{key}</p>
                <p className="text-xl font-bold">{data.value}</p>
                <p className="text-xs text-gray-500">{`제공: ${data.sites.length}개 사이트`}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Unique Stats */}
      <Card>
        <CardHeader>
          <CardTitle>객관적 지표 (특정 사이트 전용)</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {data.uniqueStats.map((stat, index) => (
              <div key={index} className="p-4 bg-gray-50 rounded">
                <p className="text-sm text-gray-600">{stat.stat}</p>
                <p className="text-xl font-bold">{stat.value}</p>
                <p className="text-xs text-gray-500">출처: {stat.source}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Subjective Metrics */}
      <Card>
        <CardHeader>
          <CardTitle>주관적 지표 비교</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {data.subjectiveData.map((metricData, index) => (
              <div key={index} className="space-y-2">
                <div className="flex justify-between items-center">
                  <h3 className="font-semibold">{metricData.metric}</h3>
                  <span className="text-sm text-gray-500">평균: {metricData.average.toFixed(2)}</span>
                </div>
                <div className="h-48">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                      data={transformMetricData(metricData)}
                      margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
                    >
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="site" />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="value" fill="#8884d8" name="평가점수" />
                      <ReferenceLine 
                        y={metricData.average} 
                        stroke="#ff0000" 
                        strokeWidth={2}
                      >
                        <Label 
                          value={`평균: ${metricData.average.toFixed(2)}`}
                          position="right"
                          fill="#ff0000"
                          fontSize={12}
                          fontWeight="bold"
                        />
                      </ReferenceLine>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

{/* Recent Matches */}
{/* Recent Matches */}
<Card>
  <CardHeader>
    <CardTitle>최근 경기</CardTitle>
  </CardHeader>
  <CardContent>
    <div className="space-y-4">
      {data.recentMatches.map((match, index) => (
        <div key={index} className="p-4 bg-gray-50 rounded grid grid-cols-9 gap-4 items-center">
          <div className="text-center whitespace-nowrap">
            <p className="text-sm text-gray-600">{match.date}</p>
          </div>
          <div className="text-center col-span-2">
            <p className="font-semibold">{match.opponent}</p>
          </div>
          <div className="text-center whitespace-nowrap">
            <p className="font-bold">{match.result}</p>
          </div>
          <div className="text-center whitespace-nowrap">
            <p className="text-sm text-gray-600">{match.minutesPlayed}분 출전</p>
          </div>
          <div className="text-center">
            <p className="text-sm font-medium">{match.goals}</p>
            <p className="text-xs text-gray-500">골</p>
          </div>
          <div className="text-center">
            <p className="text-sm font-medium">{match.assists}</p>
            <p className="text-xs text-gray-500">어시스트</p>
          </div>
          <div className="text-center">
            <div className="flex justify-center gap-2">
              <div>
                <p className="text-sm font-medium text-yellow-500">{match.yellowCards}</p>
                <p className="text-xs text-gray-500">경고</p>
              </div>
              <div>
                <p className="text-sm font-medium text-red-500">{match.redCards}</p>
                <p className="text-xs text-gray-500">퇴장</p>
              </div>
            </div>
          </div>
          <div className="text-center">
            <p className="text-xl font-bold">{match.rating.toFixed(1)}</p>
            <p className="text-xs text-gray-500">평점</p>
          </div>
        </div>
      ))}
    </div>
  </CardContent>
</Card>
    </div>
  );
};

export default PlayerDashboard;