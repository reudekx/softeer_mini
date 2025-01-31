import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "./components/ui/card";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts';
import { User, Activity, Target } from 'lucide-react';

const PlayerDashboard = () => {
  // 객관적 지표 (사이트 간 공통 데이터)
  const commonStats = {
    goals: { value: 4, sites: ['WhoScored', 'FotMob', 'SofaScore', 'FBref', 'Transfermarkt', 'Opta'] },
    assists: { value: 2, sites: ['WhoScored', 'FotMob', 'SofaScore', 'FBref', 'Transfermarkt', 'Opta'] },
    appearances: { value: 21, sites: ['WhoScored', 'FotMob', 'SofaScore', 'FBref', 'Transfermarkt', 'Opta'] },
    minutesPlayed: { value: 1363, sites: ['WhoScored', 'FotMob', 'SofaScore', 'FBref', 'Transfermarkt', 'Opta'] }
  };

  // 객관적 지표 (특정 사이트만 제공)
  const uniqueStats = [
    { stat: '패스 정확도', value: '90.1%', source: 'FBref' },
    { stat: '터치', value: '860', source: 'SofaScore' },
    { stat: '드리블 성공률', value: '56.5%', source: 'Opta' },
    { stat: '기회 창출', value: '18', source: 'FBref' }
  ];

  // 주관적 지표 (사이트별 평가)
  const subjectiveData = [
    {
      metric: 'Match Rating',
      FotMob: 6.99,
      SofaScore: 6.70,
      FBref: 6.80,
      average: 6.83
    },
    {
      metric: 'Expected Goals (xG)',
      Understat: 3.30,
      FBref: 3.35,
      Opta: 3.40, 
      average: 3.35
    },
    {
      metric: 'Expected Assists (xA)',
      Understat: 1.10,
      FBref: 1.47,
      Opta: 1.30,
      average: 1.29
    }
  ];

  // 평균 평점에 따른 상태 결정 함수
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

  const averageRating = subjectiveData.find(data => data.metric === 'Match Rating')?.average || 0;
  const status = getPlayerStatus(averageRating);

  return (
    <div className="w-full max-w-3xl mx-auto p-4 space-y-4 bg-gray-50">
      {/* Header */}
      <div className="flex items-center space-x-4 bg-white p-6 rounded-lg shadow">
        <div className="w-24 h-24 bg-gray-200 rounded-full flex items-center justify-center">
          <User size={48} />
        </div>
        <div className="flex-grow">
          <h1 className="text-2xl font-bold">에밀 스미스 로우 (Emile Smith Rowe)</h1>
          <p className="text-gray-600">풀럼 | 공격형 미드필더</p>
          <div className="mt-2">
            <span className="text-sm text-gray-500">데이터 출처: WhoScored, FotMob, SofaScore, FBref, Transfermarkt, Opta</span>
          </div>
        </div>
        <div className={`px-4 py-2 rounded-lg ${status.bgColor}`}>
          <p className={`text-3xl font-bold ${status.color}`}>{status.text}</p>
          <p className="text-sm text-gray-600">평균 평점: {averageRating.toFixed(2)}</p>
        </div>
      </div>

      {/* 객관적 지표 - 공통 데이터 */}
      <Card>
        <CardHeader>
          <CardTitle>객관적 지표 (전체 사이트 공통)</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {Object.entries(commonStats).map(([key, data]) => (
              <div key={key} className="p-4 bg-gray-50 rounded">
                <p className="text-sm text-gray-600">{key}</p>
                <p className="text-xl font-bold">{data.value}</p>
                <p className="text-xs text-gray-500">{`제공: ${data.sites.length}개 사이트`}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* 객관적 지표 - 특정 사이트 전용 */}
      <Card>
        <CardHeader>
          <CardTitle>객관적 지표 (특정 사이트 전용)</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {uniqueStats.map((stat, index) => (
              <div key={index} className="p-4 bg-gray-50 rounded">
                <p className="text-sm text-gray-600">{stat.stat}</p>
                <p className="text-xl font-bold">{stat.value}</p>
                <p className="text-xs text-gray-500">출처: {stat.source}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* 주관적 지표 비교 */}
      <Card>
        <CardHeader>
          <CardTitle>주관적 지표 비교</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            {subjectiveData.map((data, index) => (
              <div key={index} className="space-y-2">
                <h3 className="font-semibold">{data.metric}</h3>
                <div className="grid grid-cols-4 gap-4">
                  {Object.entries(data).filter(([key]) => key !== 'metric').map(([site, value]) => (
                    <div key={site} className="p-4 bg-gray-50 rounded">
                      <p className="text-sm font-medium">{site}</p>
                      <p className="text-xl font-bold">{value.toFixed(2)}</p>
                      {site === 'average' && (
                        <p className="text-xs text-blue-600">전체 평균</p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* 사이트별 데이터 제공 현황 */}
      <Card>
        <CardHeader>
          <CardTitle>사이트별 데이터 제공 현황</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 bg-gray-50 rounded">
              <h3 className="font-semibold mb-2">FotMob</h3>
              <p className="text-sm">• 선수 특성 백분율</p>
              <p className="text-sm">• 실시간 경기 데이터</p>
            </div>
            <div className="p-4 bg-gray-50 rounded">
              <h3 className="font-semibold mb-2">FBref</h3>
              <p className="text-sm">• xG/xA 상세 통계</p>
              <p className="text-sm">• 패스 완성도 분석</p>
            </div>
            <div className="p-4 bg-gray-50 rounded">
              <h3 className="font-semibold mb-2">SofaScore</h3>
              <p className="text-sm">• 터치 맵 데이터</p>
              <p className="text-sm">• 포지셔널 히트맵</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default PlayerDashboard;