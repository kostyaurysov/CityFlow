import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import java.io.IOException;

public class ImeiSet {
    public static class Map extends Mapper<LongWritable, Text, Text, Text> {
        private Text imei = new Text();
        private Text data = new Text();

        public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
            String line = value.toString();
            String[] splittedLine = line.split(",");
            if(splittedLine.length >19) {
                if (!splittedLine[18].equals("NULL")) {
                    if(!splittedLine[19].equals("NULL")) {
                        if(!splittedLine[0].equals("NULL")) {
                            if(splittedLine[0].length() > 23) {
                                StringBuilder sb = new StringBuilder();
                                sb.append(splittedLine[18]);
                                sb.append(";");
                                sb.append(splittedLine[19]);
                                sb.append(";");
                                sb.append(splittedLine[0]);
                                imei.set(splittedLine[4]);
                                data.set(sb.toString());
                                context.write(imei, data);
                            }
                        }
                    }
                }
            }
        }
    }
    public static class Reduce extends Reducer<Text, Text, Text, Text> {
        public void reduce(Text key, Iterable<Text> values, Context context)
                throws IOException, InterruptedException {
            Text sum = new Text();

            StringBuilder sb = new StringBuilder();
            for (Text val : values) {
                sb.append(val.toString());
                sb.append(",");
            }
            sb.deleteCharAt(sb.length() - 1);
            sum.set(sb.toString());
            context.write(key, sum);
        }
    }
    public static void main(String[] args) throws IOException, ClassNotFoundException, InterruptedException {
        Configuration conf = new Configuration();
        Job job = new Job(conf, "wordcount");
        job.setJarByClass(ImeiSet.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);
        job.setMapperClass(Map.class);
        job.setReducerClass(Reduce.class);
        job.setInputFormatClass(TextInputFormat.class);
        job.setOutputFormatClass(TextOutputFormat.class);
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        job.waitForCompletion(true);
    }
}