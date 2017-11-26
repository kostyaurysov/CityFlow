import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;

public class ImeiTrashMapping {
    public static class Map extends Mapper<LongWritable, Text, Text, IntWritable> {
        private Text data = new Text();
        private IntWritable count = new IntWritable(1);

        public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
            FileReader fr = new FileReader("bin_filtered_with_gps.csv");
            BufferedReader bufr = new BufferedReader(fr);

            String line = value.toString();
            String[] splittedLine = line.split("\t");
            String[] splittedCoordinates = splittedLine[1].split(",");
            for (int i = 0; i < splittedCoordinates.length; i++) {
                String[] coordinates = splittedCoordinates[i].split(";");
                double lat2 = Double.valueOf(coordinates[0]);
                double lon2 = Double.valueOf(coordinates[1]);
                String binCoordinates = bufr.readLine();

                while (binCoordinates != null) {
                    String[] splittedBinCoordinates = binCoordinates.split(";");

                    double lat1 = Double.valueOf(splittedBinCoordinates[0]);
                    double lon1 = Double.valueOf(splittedBinCoordinates[1]);
                    double distance = distanceBetweenPoints(lat1, lon1, lat2, lon2);
                    data.set(lat1 + ":" + lon1);
                    if(distance < 100) {
                        context.write(data, count);
                    }
                    binCoordinates = bufr.readLine();
                }
            }
        }
    }

    public static double distanceBetweenPoints(double lat1, double lon1, double lat2, double lon2) {
        double R = 6371e3;
        double phi1 = Math.toRadians(lat1);
        double phi2 = Math.toRadians(lat2);
        double deltaPhi = Math.toRadians(lat2 - lat1);
        double deltaLambda = Math.toRadians(lon2 - lon1);
        double a = Math.sin(deltaPhi / 2) * Math.sin(deltaPhi / 2) + Math.cos(phi1) * Math.cos(phi2) * Math.sin(deltaLambda / 2) * Math.sin(deltaLambda / 2);
        double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        return R * c;
    }

    public static class Reduce extends Reducer<Text, IntWritable, Text, IntWritable> {

        private IntWritable result = new IntWritable();

        public void reduce(Text key, Iterable<IntWritable> values, Context context)
                throws IOException, InterruptedException {
            int sum = 0;
            for (IntWritable val : values) {
                sum += val.get();
            }
            result.set(sum);
            context.write(key, result);
        }
    }
    public static void main(String[] args) throws IOException, ClassNotFoundException, InterruptedException {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "peoplecount");
        job.setJarByClass(ImeiTrashMapping.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        job.setMapperClass(Map.class);
        job.setReducerClass(Reduce.class);

        job.setInputFormatClass(TextInputFormat.class);
        job.setOutputFormatClass(TextOutputFormat.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}